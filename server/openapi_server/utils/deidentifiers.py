from typing import List, Dict
from openapi_server.models import Note


def apply_mask(deidentified_note, annotation, left_shifts, mask):
    # Account for shift caused by replacement
    start = annotation['start'] - left_shifts[annotation['start']]
    end = annotation['start'] + annotation['length'] - left_shifts[annotation['start'] + annotation['length']]
    length = end - start

    # Replace each annotation in note with "[ANNOTATION_TYPE_HERE]"
    deidentified_note.text = \
        deidentified_note.text[:start] + \
        mask + \
        deidentified_note.text[end:]

    for i in range(annotation['start'] + 1, len(left_shifts)):
        left_shifts[i] += min(i - annotation['start'] - len(mask), length - len(mask))


def update_annotations(annotations, left_shifts):
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
    return deidentified_annotations


def apply_deidentification(annotation_types, annotations, confidence_threshold, note, masker):
    left_shifts = [0] * (len(note.text) + 1)
    deidentified_note = Note(
        note_type=note.note_type,
        text=note.text,
        patient_id=note.patient_id,
        id=note.id
    )
    for annotation_type in annotation_types:
        # Only de-identify notes with sufficient confidence level
        annotation_set = [annotation for annotation in annotations[annotation_type] if
                          annotation['confidence'] >= confidence_threshold]
        for annotation in annotation_set:
            annotation['type'] = annotation_type
            mask = masker(annotation)
            # Record left shift introduced by redaction
            apply_mask(deidentified_note, annotation, left_shifts, mask)
    # Update deidentified annotations with appropriate left shifts
    deidentified_annotations = update_annotations(annotations, left_shifts)
    return deidentified_annotations, deidentified_note


def apply_masking_char(note: Note, annotations, confidence_threshold, annotation_types: List[str], masking_char='*'):
    """
    Apply a masking character de-identification to a note for the given annotation types

    :param note: note to be de-identified
    :param annotations: (dict: annotation_type -> [annotation])
    :param confidence_threshold: (float, 0 <= confidence_threshold <= 100) minimum confidence level required to apply an annotation
    :param annotation_types: list of types of annotations to be masked
    :param masking_char: the character used to mask PII
    :return: (note, deidentified_annotations) note with de-identified text, and annotations.
    """
    deidentified_annotations, deidentified_note = apply_deidentification(
        annotation_types,
        annotations,
        confidence_threshold,
        note,
        masker=lambda annotation: len(annotation['text']) * masking_char
    )
    return deidentified_note, deidentified_annotations


def apply_redaction(note: Note, annotations, confidence_threshold, annotation_types: List[str]):
    """
    Apply redaction to a note for the given annotation types

    :param note: note to be de-identified
    :param annotations: (dict: annotation_type -> [annotation])
    :param confidence_threshold: (float, 0 <= confidence_threshold <= 100) minimum confidence level required to apply an annotation
    :param annotation_types: list of types of annotations to be redacted
    :return: (note, deidentified_annotations) note with de-identified text, and annotations now pointing to
            corrected character addresses.
    """
    deidentified_annotations, deidentified_note = apply_deidentification(annotation_types, annotations,
                                                                         confidence_threshold, note,
                                                                         masker=lambda annotation: '')
    return deidentified_note, deidentified_annotations


def apply_annotation_type(note: Note, annotations, confidence_threshold, annotation_types: List[str]):
    """
    Apply annotation-type de-identification to a note for the given annotation types

    :param note: note to be de-identified
    :param annotations: (dict: annotation_type -> [annotation])
    :param confidence_threshold: (float, 0 <= confidence_threshold <= 100) minimum confidence level required to apply an annotation
    :param annotation_types: list of types of annotations to be redacted
    :return: (note, deidentified_annotations) note with de-identified text, and annotations now pointing to
            corrected character addresses.
    """
    deidentified_annotations, deidentified_note = apply_deidentification(
        annotation_types,
        annotations,
        confidence_threshold,
        note,
        masker=lambda annotation: '[%s]' % (annotation['type'].upper(),)
    )
    return deidentified_note, deidentified_annotations
