import requests

from openapi_server.models import Note

URLS = {
    'text_date': 'http://date-annotator:8080/api/v1/textDateAnnotations',
    'text_person_name': 'http://person-name-annotator:8080/api/v1/textPersonNameAnnotations',
    'text_physical_address': 'http://physical-address-annotator:8080/api/v1/textPhysicalAddressAnnotations'
}
CAMEL_CASE = {
    'text_date': 'textDateAnnotations',
    'text_person_name': 'textPersonNameAnnotations',
    'text_physical_address': 'textPhysicalAddressAnnotations'
}


def get_annotations(note: Note, annotation_type: str):
    response = requests.post(
        url=URLS[annotation_type],
        json={'note': {
            'noteType': note.note_type,
            'text': note.text
        }},
        headers={'Content-Type': 'application/json', 'charset': 'utf-8'}
    )
    return response.json()[CAMEL_CASE[annotation_type]]
