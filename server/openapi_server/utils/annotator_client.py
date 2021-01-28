import requests
from urllib.parse import urljoin
from openapi_server.models import Note
from openapi_server.models import Tool, ToolDependencies


BASE_URLS = {
    'text_date': 'http://date-annotator:8080/api/v1/',
    'text_person_name': 'http://person-name-annotator:8080/api/v1/',
    'text_physical_address': 'http://physical-address-annotator:8080/api/v1/'
}


CAMEL_CASE = {
    'text_date': 'textDateAnnotations',
    'text_person_name': 'textPersonNameAnnotations',
    'text_physical_address': 'textPhysicalAddressAnnotations'
}


def get_tool_dependencies():
    tool_dependencies = []
    for annotation_type, base_url in BASE_URLS.items():
        response = requests.get(
            url=urljoin(base_url, 'tool'),
            headers={
                'Content-Type': 'application/json',
                'charset': 'utf-8'
            }
        )
        tool = Tool.from_dict(response.json())
        tool_dependencies.append(tool)
    return tool_dependencies


def get_annotations(note: Note, annotation_type: str):
    url = urljoin(BASE_URLS[annotation_type], CAMEL_CASE[annotation_type])
    response = requests.post(
        url=url,
        json={'note': {
            'noteType': note.note_type,
            'text': note.text
        }},
        headers={'Content-Type': 'application/json', 'charset': 'utf-8'}
    )
    return response.json()[CAMEL_CASE[annotation_type]]
