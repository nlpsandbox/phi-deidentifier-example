import connexion

from openapi_server.models import DeidentificationConfig
from openapi_server.models.deidentify_request import DeidentifyRequest  # noqa: E501
from openapi_server.models.note import Note  # noqa: E501
from openapi_server.utils import annotator_client
from openapi_server.utils.deidentifiers import apply_masking_char, apply_redaction, apply_annotation_type


def create_deidentified_notes():  # noqa: E501
    """Deidentify a clinical note

    Returns the deidentified note # noqa: E501

    :param deidentify_request: 
    :type deidentify_request: dict | bytes

    :rtype: DeidentifyResponse
    """

    if connexion.request.is_json:
        deid_request = DeidentifyRequest.from_dict(connexion.request.get_json())
        note = deid_request.note

        annotations = {}

        for annotation_type in ['text_date', 'text_person_name', 'text_physical_address']:
            annotations[annotation_type] = annotator_client.get_annotations(note, annotation_type)

        # De-identify note
        deidentified_note = Note.from_dict(note.to_dict())
        # FIXME: Following should be deep copy
        deidentified_annotations = annotations.copy()

        deid_config: DeidentificationConfig
        for deid_config in deid_request.deidentification_configurations:
            if deid_config.deidentification_strategy.masking_char_config is not None:
                masking_char = deid_config.deidentification_strategy.masking_char_config.masking_char
                deidentified_note, deidentified_annotations = apply_masking_char(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config.annotation_types,
                    masking_char
                )
            elif deid_config.deidentification_strategy.redact_config is not None:
                deidentified_note, deidentified_annotations = apply_redaction(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config.annotation_types
                )
            elif deid_config.deidentification_strategy.annotation_type_config is not None:
                deidentified_note, deidentified_annotations = apply_annotation_type(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config.annotation_types
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
