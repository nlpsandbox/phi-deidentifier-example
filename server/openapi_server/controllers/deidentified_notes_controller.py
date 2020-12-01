import connexion
import six
from flask import jsonify
import requests

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
    FIXME: Currently just does a masking character de-identify on all annotation types
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
    :param masking_char: the character used to mask PII
    :return (deidentified_note, deidentified_annotations): note with de-identified text, and annotations now pointing to
            corrected character addresses (in case of redaction or annotation type de-identification).
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
