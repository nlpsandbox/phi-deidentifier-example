import connexion

from openapi_server.models import DeidentificationConfig, DeidentifyResponse, Annotation
from openapi_server.models.deidentify_request import DeidentifyRequest  # noqa: E501
from openapi_server.models.note import Note  # noqa: E501
from openapi_server.utils import annotators
from openapi_server.utils.deidentifiers import apply_masking_char, apply_redaction, apply_annotation_type


def create_deidentified_notes():  # noqa: E501
    """Deidentify a clinical note

    Returns the deidentified note # noqa: E501

    :rtype: DeidentifyResponse
    """

    if connexion.request.is_json:
        deid_request = DeidentifyRequest.from_dict(connexion.request.get_json())
        note = deid_request.note

        # Annotations is a dict[key: list[str]]
        annotations = {}

        for annotation_type in ['text_date', 'text_person_name', 'text_physical_address']:
            annotations[annotation_type] = annotators.annotate(note, annotation_type)

        # De-identify note
        deidentified_note = Note.from_dict(note.to_dict())
        deidentified_annotations = {key: value.copy() for key, value in annotations.items()}

        deid_config: DeidentificationConfig
        for deid_config in deid_request.deidentification_configurations:
            if deid_config.deidentification_strategy.masking_char_config is not None:
                masking_char = deid_config.deidentification_strategy.masking_char_config.masking_char
                deidentified_note, deidentified_annotations = apply_masking_char(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config.confidence_threshold,
                    deid_config.annotation_types,
                    masking_char
                )
            elif deid_config.deidentification_strategy.redact_config is not None:
                deidentified_note, deidentified_annotations = apply_redaction(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config.confidence_threshold,
                    deid_config.annotation_types
                )
            elif deid_config.deidentification_strategy.annotation_type_config is not None:
                deidentified_note, deidentified_annotations = apply_annotation_type(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config.confidence_threshold,
                    deid_config.annotation_types
                )
            else:
                return "No supported de-identification method supported in request: '%s'" % (str(deid_config.to_dict()),), 400

        deidentify_response = DeidentifyResponse(
            deidentified_note=deidentified_note,
            original_annotations=Annotation(
                text_date_annotations=annotations['text_date'],
                text_person_name_annotations=annotations['text_person_name'],
                text_physical_address_annotations=annotations['text_physical_address']
            ),
            deidentified_annotations=Annotation(
                text_date_annotations=deidentified_annotations['text_date'],
                text_person_name_annotations=deidentified_annotations['text_person_name'],
                text_physical_address_annotations=deidentified_annotations['text_physical_address']
            )
        )
        return deidentify_response, 200
