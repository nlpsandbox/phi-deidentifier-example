import connexion
from datanode.model.note_id import NoteId
from datanode.model.patient_id import PatientId

from openapi_server.models.deidentify_request import DeidentifyRequest  # noqa: E501
from openapi_server.models import DeidentificationStep, DeidentifyResponse, \
    AnnotationSet, Note
from openapi_server.phi_deidentifier.deidentifiers import apply_masking_char, \
    apply_redaction, apply_annotation_type
from openapi_server.config import Config
from nlpsandboxclient import client


def create_deidentified_notes(deidentify_request=None):  # noqa: E501
    """Deidentify a clinical note

    Returns the deidentified note # noqa: E501

    :param deidentify_request:
    :type deidentify_request: dict | bytes

    :rtype: DeidentifyResponse
    """
    if connexion.request.is_json:
        deid_request = DeidentifyRequest.from_dict(
            connexion.request.get_json())
        note = deid_request.note

        # Make set of all annotation types in the de-id request
        all_annotation_types = {
            annotation_type for annotation_types in
            [deid_step.annotation_types for deid_step
             in deid_request.deidentification_steps]
            for annotation_type in annotation_types
        }

        config = Config()
        # Annotations is a dict[key: list[str]]
        annotations = {'text_date': [], 'text_person_name': [],
                       'text_physical_address': [], 'text_contact': [],
                       'text_id': []}

        # Convert to NLPSandboxClient's Note object
        client_note = client.Note(
            identifier=NoteId(note.identifier), text=note.text, type=note.type,
            patient_id=PatientId(note.patient_id))

        if 'text_date' in all_annotation_types:
            annotations['text_date'] = client.annotate_note(
                host=config.date_annotator_api_url,
                note=client_note, tool_type='nlpsandbox:date-annotator')[
                'textDateAnnotations']
        if 'text_person_name' in all_annotation_types:
            annotations['text_person_name'] = client.annotate_note(
                host=config.person_name_annotator_api_url,
                note=client_note, tool_type='nlpsandbox:person-name-annotator')[
                'textPersonNameAnnotations']
        if 'text_physical_address' in all_annotation_types:
            annotations['text_physical_address'] = client.annotate_note(
                host=config.physical_address_annotator_api_url,
                note=client_note,
                tool_type='nlpsandbox:physical-address-annotator')[
                'textPhysicalAddressAnnotations']
        if 'text_contact' in all_annotation_types:
            annotations['text_contact'] = client.annotate_note(
                host=config.contact_annotator_api_url,
                note=client_note,
                tool_type='nlpsandbox:contact-annotator')[
                'textContactAnnotations']
        if 'text_id' in all_annotation_types:
            annotations['text_id'] = client.annotate_note(
                host=config.id_annotator_api_url,
                note=client_note,
                tool_type='nlpsandbox:id-annotator')[
                'textIdAnnotations']

        # De-identify note
        deidentified_note = \
            Note.from_dict({note.attribute_map[key]: value for key, value
                            in note.to_dict().items()})
        deidentified_annotations = \
            {key: value.copy() for key, value in annotations.items()}

        deid_config: DeidentificationStep
        for deid_config in deid_request.deidentification_steps:
            if deid_config.masking_char_config is not None:
                masking_char = \
                    deid_config.masking_char_config.masking_char
                deidentified_note, deidentified_annotations = \
                    apply_masking_char(
                        deidentified_note,
                        deidentified_annotations,
                        deid_config.confidence_threshold,
                        deid_config.annotation_types,
                        masking_char
                    )
            elif deid_config.redact_config \
                    is not None:
                deidentified_note, deidentified_annotations = apply_redaction(
                    deidentified_note,
                    deidentified_annotations,
                    deid_config.confidence_threshold,
                    deid_config.annotation_types
                )
            elif deid_config.annotation_type_mask_config \
                    is not None:
                deidentified_note, deidentified_annotations = \
                    apply_annotation_type(
                        deidentified_note,
                        deidentified_annotations,
                        deid_config.confidence_threshold,
                        deid_config.annotation_types
                    )
            else:
                return "No supported de-identification method supported in " \
                       "request: '%s'" % (
                           str(deid_config.to_dict()),), 400

        deidentify_response = DeidentifyResponse(
            deidentified_note=deidentified_note,
            original_annotations=AnnotationSet(
                text_date_annotations=annotations['text_date'],
                text_person_name_annotations=annotations['text_person_name'],
                text_physical_address_annotations=annotations[
                    'text_physical_address'],
                text_contact_annotations=annotations[
                    'text_contact_annotations'],
                text_id_annotations=annotations['text_id_annotations'],
            ),
            deidentified_annotations=AnnotationSet(
                text_date_annotations=deidentified_annotations['text_date'],
                text_person_name_annotations=deidentified_annotations[
                    'text_person_name'],
                text_physical_address_annotations=deidentified_annotations[
                    'text_physical_address']
            )
        )
        return deidentify_response, 200
