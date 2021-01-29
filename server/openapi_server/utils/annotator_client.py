import requests
from openapi_server.models import Note, Tool, ToolDependencies
from openapi_server.config import Config


BASE_URLS = {
    'text_date': Config().date_annotator_api_url,
    'text_person_name': Config().person_name_annotator_api_url,
    'text_physical_address': Config().physical_address_annotator_api_url
}


CAMEL_CASE = {
    'text_date': 'textDateAnnotations',
    'text_person_name': 'textPersonNameAnnotations',
    'text_physical_address': 'textPhysicalAddressAnnotations'
}


TOOL_URL = 'tool'


def get_annotations(note: Note, annotation_type: str):
    url = '%s/%s' % (BASE_URLS[annotation_type], CAMEL_CASE[annotation_type])
    response = requests.post(
        url=url,
        json=note.to_dict(),
        headers={'Content-Type': 'application/json', 'charset': 'utf-8'}
    )
    return response.json()[CAMEL_CASE[annotation_type]]


def get_annotators_info():
    tools = []
    for annotation_type, base_url in BASE_URLS.items():
        url = '%s/%s' % (BASE_URLS[annotation_type], TOOL_URL)
        response = requests.get(
            url=url,
            headers={'Content-Type': 'application/json', 'charset': 'utf-8'}
        )
        tools.append(Tool.from_dict(response.json()))
    tool_dependencies = ToolDependencies(tool_dependencies=tools)
    return tool_dependencies