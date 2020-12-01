import connexion
import six
from flask import jsonify
import requests

from openapi_server.models.deidentify_request import DeidentifyRequest  # noqa: E501
from openapi_server.models.deidentify_response import DeidentifyResponse  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.note import Note  # noqa: E501
from openapi_server import util


def create_deidentified_notes(deidentify_request=None):  # noqa: E501
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
        deidentification_request: DeidentifyRequest = connexion.request.get_json()
        note = deidentification_request['note']

        """
        dates = []
        person_names = []
        physical_addresses = []
        """

        # Get date annotations
        response = requests_session.post(url=dates_url, json={'note': note})
        if response.status_code == 200:
            dates = response.json()['textDateAnnotations']
        else:
            return "failed on date-annotator"

        # Get person name annotations
        response = requests_session.post(url=person_names_url, json={'note': note})
        if response.status_code == 200:
            person_names = response.json()['textPersonNameAnnotations']
        else:
            return "failed on name-annotator: %s" % (repr(response),)

        # Get physical address annotations
        response = requests_session.post(url=physical_addresses_url, json={'note': note})
        if response.status_code == 200:
            physical_addresses = response.json()['textPhysicalAddressAnnotations']
        else:
            return "failed on address-annotator"

        # De-identify note
        deid_text = apply_masking_char(note, dates, person_names, physical_addresses)

        return deid_text


def apply_masking_char(note, dates, person_names, physical_addresses):
    """
    Returns the deidentified clinical note where annotations are masked with '*'.
    """
    mask_character = '*'
    text = note['text']

    for annotation in dates:
        mask = mask_character * annotation['length']
        text = text[:annotation['start']] + mask + text[annotation['start'] + annotation['length']:]

    for annotation in person_names:
        mask = mask_character * annotation['length']
        text = text[:annotation['start']] + mask + text[annotation['start'] + annotation['length']:]

    for annotation in physical_addresses:
        mask = mask_character * annotation['length']
        text = text[:annotation['start']] + mask + text[annotation['start'] + annotation['length']:]

    return text
