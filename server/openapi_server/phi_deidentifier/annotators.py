import requests
from openapi_server.models import Note, Tool, ToolDependencies
from openapi_server.config import Config


BASE_URLS = {
    'text_date': Config().date_annotator_api_url,
    'text_person_name': Config().person_name_annotator_api_url,
    'text_physical_address': Config().physical_address_annotator_api_url
}


ANNOTATION_TYPES_CAMEL_CASE = {
    'text_date': 'textDateAnnotations',
    'text_person_name': 'textPersonNameAnnotations',
    'text_physical_address': 'textPhysicalAddressAnnotations'
}


TOOL_URL_PATH = 'tool'


def annotate(note: Note, annotation_type: str):
    url = '%s/%s' % (BASE_URLS[annotation_type], ANNOTATION_TYPES_CAMEL_CASE[annotation_type])
    response = requests.post(
        url=url,
        json={'note': {note.attribute_map[key]: value for key, value in note.to_dict().items() if value is not None}},
        headers={'Content-Type': 'application/json', 'charset': 'utf-8'}
    )
    return response.json()[ANNOTATION_TYPES_CAMEL_CASE[annotation_type]]


def get_annotators_info():
    tools = []
    for annotation_type, base_url in BASE_URLS.items():
        url = '%s/%s' % (BASE_URLS[annotation_type], TOOL_URL_PATH)
        response = requests.get(
            url=url,
            headers={'Content-Type': 'application/json', 'charset': 'utf-8'}
        )
        tools.append(Tool.from_dict(response.json()))
    tool_dependencies = ToolDependencies(tool_dependencies=tools)
    return tool_dependencies

