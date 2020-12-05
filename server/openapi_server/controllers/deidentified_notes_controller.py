import connexion
import six
from flask import jsonify
import requests
import sys

from openapi_server.models.deidentify_request import DeidentifyRequest  # noqa: E501
from openapi_server.models.deidentify_response import DeidentifyResponse  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.note import Note  # noqa: E501
from openapi_server import util


def create_deidentified_notes():  # noqa: E501
    """Deidentify a clinical note

    Returns the deidentified note # noqa: E501

    :param deidentify_request: 
    :type deidentify_request: dict | bytes

    :rtype: DeidentifyResponse
    FIXME: Currently can only do masking character and redact de-identifications
    """
    res = []

    # for testing when annotator are running as containers
    dates_url = "http://date-annotator:8080/api/v1/textDateAnnotations"
    person_names_url = "http://person-name-annotator:8080/api/v1/textPersonNameAnnotations"
    physical_addresses_url = "http://physical-address-annotator:8080/api/v1/textPhysicalAddressAnnotations"

    requests_session = requests.session()
    requests_session.headers.update({'Content-Type': 'application/json'})
    requests_session.headers.update({'charset':'utf-8'})

    if connexion.request.is_json:
        deidentify_request = connexion.request.get_json()
        note = deidentify_request['note']

        annotations = {}

        # Get date annotations
        response = requests_session.post(url=dates_url, json={'note': note})
        if response.status_code == 200:
            annotations['text_date'] = response.json()['textDateAnnotations']

        # Get person name annotations
        response = requests_session.post(url=person_names_url, json={'note': note})
        if response.status_code == 200:
            annotations['text_person_name'] = response.json()['textPersonNameAnnotations']

        # Get physical address annotations
        response = requests_session.post(url=physical_addresses_url, json={'note': note})
        if response.status_code == 200:
            annotations['text_physical_address'] = response.json()['textPhysicalAddressAnnotations']

        # De-identify note
        deidentified_note = note.copy()
        # FIXME: Following should be deep copy
        deidentified_annotations = annotations.copy()
        for deid_config in deidentify_request['deidentificationConfigurations']:
            if 'maskingCharConfig' in deid_config['deidentificationStrategy']:
                masking_char = deid_config['deidentificationStrategy']['maskingCharConfig']['maskingChar']
                deidentified_note, deidentified_annotations = apply_masking_char(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config['annotationTypes'],
                    masking_char
                )
            elif 'redactConfig' in deid_config['deidentificationStrategy']:
                deidentified_note, deidentified_annotations = apply_redaction(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config['annotationTypes']
                )
            elif 'annotationTypeConfig' in deid_config['deidentificationStrategy']:
                deidentified_note, deidentified_annotations = apply_annotation_type(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config['annotationTypes']
                )
            else:
                # Handle other deid methods in elif's
                pass

        return {
            'note': deidentified_note,
            'originalAnnotations': {
                'textDateAnnotations': annotations['text_date'],
                'textPersonNameAnnotations': annotations['text_person_name'],
                'textPhysicalAddressAnnotations': annotations['text_physical_address']
            },
            'deidentifiedAnnotations': {
                'textDateAnnotations': deidentified_annotations['text_date'],
                'textPersonNameAnnotations': deidentified_annotations['text_person_name'],
                'textPhysicalAddressAnnotations': deidentified_annotations['text_physical_address']
            },
        }


def apply_masking_char(note, annotations, annotation_types, masking_char='*'):
    """
    Apply a masking character de-identification to a note for the given annotation types

    :param note: note to be de-identified
    :param annotations: (dict: annotation_type -> [annotation])
    :param annotation_types: list of types of annotations to be masked
    :param masking_char: the character used to mask PII
    :return: (deidentified_note, deidentified_annotations) note with de-identified text, and annotations.
    """
    deidentified_note = note.copy()
    deidentified_annotations = annotations.copy()  # Masking char doesn't change any character addresses

    for annotation_type in annotation_types:
        annotation_set = annotations[annotation_type]
        for annotation in annotation_set:
            mask = masking_char * annotation['length']
            deidentified_note['text'] = \
                deidentified_note['text'][:annotation['start']] + \
                mask + \
                deidentified_note['text'][annotation['start'] + annotation['length']:]

    return deidentified_note, deidentified_annotations


def apply_redaction(note, annotations, annotation_types):
    """
    Apply redaction to a note for the given annotation types

    :param note: note to be de-identified
    :param annotations: (dict: annotation_type -> [annotation])
    :param annotation_types: list of types of annotations to be redacted
    :return: (deidentified_note, deidentified_annotations) note with de-identified text, and annotations now pointing to
            corrected character addresses.
    """
    deidentified_note = note.copy()
    left_shifts = [0] * len(note['text'])

    for annotation_type in annotation_types:
        for annotation in annotations[annotation_type]:
            # Account for shift caused by redaction
            start = annotation['start'] - left_shifts[annotation['start']]
            end = annotation['start'] + annotation['length'] - left_shifts[annotation['start'] + annotation['length']]
            length = end - start

            # Redact each annotation in note
            deidentified_note['text'] = \
                deidentified_note['text'][:start] + \
                deidentified_note['text'][start + length:]

            # Record left shift introduced by redaction
            for i in range(annotation['start'], len(left_shifts)):
                left_shifts[i] += min(i - annotation['start'], length)

    # Update deidentified annotations with appropriate left shifts
    deidentified_annotations = {annotation_type: [] for annotation_type in annotations.keys()}
    for annotation_type, annotation_set in annotations.items():
        for annotation in annotation_set:
            old_start = annotation['start']
            old_end = old_start + annotation['length']

            new_start = old_start - left_shifts[old_start]
            new_end = old_end - left_shifts[old_end]

            deidentified_annotation = annotation.copy()
            deidentified_annotation['start'] = new_start
            deidentified_annotation['length'] = new_end - new_start

            deidentified_annotations[annotation_type].append(deidentified_annotation)

    return deidentified_note, deidentified_annotations


def apply_annotation_type(note, annotations, annotation_types):
    """
    Apply annotation-type de-identification to a note for the given annotation types

    :param note: note to be de-identified
    :param annotations: (dict: annotation_type -> [annotation])
    :param annotation_types: list of types of annotations to be redacted
    :return: (deidentified_note, deidentified_annotations) note with de-identified text, and annotations now pointing to
            corrected character addresses.
    """
    deidentified_note = note.copy()
    left_shifts = [0] * len(note['text'])

    for annotation_type in annotation_types:
        for annotation in annotations[annotation_type]:
            # Account for shift caused by replacement
            start = annotation['start'] - left_shifts[annotation['start']]
            end = annotation['start'] + annotation['length'] - left_shifts[annotation['start'] + annotation['length']]
            length = end - start

            # = "[ANNOTATION_TYPE_HERE]"
            filler = "[%s]" % (annotation_type.upper(),)

            # Replace each annotation in note with "[ANNOTATION_TYPE_HERE]"
            deidentified_note['text'] = \
                deidentified_note['text'][:start] + filler +\
                deidentified_note['text'][start + length:]

            # Record left shift introduced by replacement
            # for i in range(annotation['start']+1, len(left_shifts)):
            for i in range(annotation['start']+1, len(left_shifts)):
                left_shifts[i] += min(i - annotation['start'] - len(filler), length - len(filler))

    # Update deidentified annotations with appropriate left shifts
    deidentified_annotations = {annotation_type: [] for annotation_type in annotations.keys()}
    for annotation_type, annotation_set in annotations.items():
        for annotation in annotation_set:
            old_start = annotation['start']
            old_end = old_start + annotation['length']

            new_start = old_start - left_shifts[old_start]
            new_end = old_end - left_shifts[old_end]

            deidentified_annotation = annotation.copy()
            deidentified_annotation['start'] = new_start
            deidentified_annotation['length'] = new_end - new_start

            deidentified_annotations[annotation_type].append(deidentified_annotation)

    return deidentified_note, deidentified_annotations
