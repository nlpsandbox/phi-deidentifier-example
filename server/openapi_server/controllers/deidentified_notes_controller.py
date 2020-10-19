import connexion
import six
from flask import jsonify
import requests

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.note import Note  # noqa: E501
from openapi_server import util


def deidentified_notes_read_all(note=None):  # noqa: E501
    """Get deidentified notes

    Returns the deidentified notes # noqa: E501

    :param note:
    :type note: list | bytes

    :rtype: List[Note]
    """
    res = []

    # for testing when annotator are running as containers
    dates_url = "http://date-annotator:8080/api/v1/dates"
    person_names_url = "http://person-name-annotator:8080/api/v1/person-names"

    requests_session = requests.session()
    requests_session.headers.update({'Content-Type': 'application/json'})
    requests_session.headers.update({'charset':'utf-8'})

    if connexion.request.is_json:
        dates = []
        person_names = []
        notes = connexion.request.get_json()

        # Get date annotations
        response = requests_session.post(url=dates_url, json=notes)
        if response.status_code == 200:
            dates = response.json()

        # Get person name annotations
        response = requests_session.post(url=person_names_url, json=notes)
        if response.status_code == 200:
            person_names = response.json()

        # Create deidentified notes
        for note in notes:
            note_id = note['id']
            res.append(deidentify_note(note,
                [d for d in dates if d['noteId'] == note_id],
                [d for d in person_names if d['noteId'] == note_id]))

    return jsonify(res)


def deidentify_note(note, dates, person_names):
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

    note['text'] = text
    return note