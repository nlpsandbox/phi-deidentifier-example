from openapi_server.models import Note, Tool, License

__doc__ = "Utils and sample data for testing"


ANNOTATOR_TYPE_MAP = {
    'address': ('text_physical_address', 'textPhysicalAddressAnnotations'),
    'person': ('text_person_name', 'textPersonNameAnnotations'),
    'date': ('text_date', 'textDateAnnotations')
}


SAMPLE_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "identifier": "snote",
    "patientId": "abc123",
    "text":
        "Mary Williamson came back from Seattle yesterday, 12 December 2013."
})


SAMPLE_NOTE_ANNOTATIONS = {
    'text_date': [
        {'confidence': 95, 'dateFormat': 'YYYY',
         'length': 4, 'start': 62, 'text': '2013'},
        {'confidence': 95, 'dateFormat': 'MMMM',
         'length': 8, 'start': 53, 'text': 'December'},
        {'confidence': 95, 'dateFormat': 'MMMM',
         'length': 2, 'start': 50, 'text': '12'}
    ],
    'text_person_name': [
        {'confidence': 95, 'length': 4,
         'start': 0, 'text': 'Mary'},
        {'confidence': 95, 'length': 10,
         'start': 5, 'text': 'Williamson'}
    ],
    'text_physical_address': [
        {'addressType': 'city', 'confidence': 95,
         'length': 7, 'start': 31, 'text': 'Seattle'}
    ]
}


# A note with more ambiguous PII
OVERLAPPING_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "identifier": "ono",
    "patientId": "def456",
    "text": "May Williamson came back from Austin, TX yesterday, 12 June 2013."
})


OVERLAPPING_ANNOTATIONS = {
    'text_date': [
        {'confidence': 40, 'dateFormat': 'MM',
         'length': 3, 'start': 0, 'text': 'May'},
        {'confidence': 93, 'dateFormat': 'MM',
         'length': 4, 'start': 55, 'text': 'June'},
        {'confidence': 95, 'dateFormat': 'MMMM',
         'length': 2, 'start': 52, 'text': '12'},
        {'confidence': 97, 'dateFormat': 'YYYY',
         'length': 4, 'start': 60, 'text': '2013'}
    ],
    'text_person_name': [
        {'confidence': 55, 'length': 3,
         'start': 0, 'text': 'May'},
        {'confidence': 97, 'length': 10,
         'start': 4, 'text': 'Williamson'},
        {'confidence': 60, 'length': 6,
         'start': 30, 'text': 'Austin'}
    ],
    'text_physical_address': [
        {'addressType': 'city', 'confidence': 30,
         'length': 6, 'start': 30, 'text': 'Austin'},
        {'addressType': 'state', 'confidence': 95,
         'length': 2, 'start': 38, 'text': 'TX'}
    ]
}


# A note with more ambiguous PII
CONFLICTING_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "identifier": "cnote",
    "patientId": "ghi789",
    "text": "ABCDEFG"
})


CONFLICTING_ANNOTATIONS = {
    'text_date': [
        {'confidence': 97, 'dateFormat': 'MM',
         'length': 3, 'start': 0, 'text': 'ABC'}
    ],
    'text_person_name': [
        {'confidence': 97, 'length': 4,
         'start': 0, 'text': 'ABCD'}
    ],
    'text_physical_address': [
        {'addressType': 'state', 'confidence': 97,
         'length': 5, 'start': 0, 'text': 'ABCDE'}
    ]
}


PARTIAL_OVERLAP_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "identifier": "ponote",
    "patientId": "jkl123",
    "text": "TUVWXYZ"
})


PARTIAL_OVERLAP_ANNOTATIONS = {
    'text_date': [
        {'confidence': 97, 'dateFormat': 'MM',
         'length': 3, 'start': 0, 'text': 'TUV'}
    ],
    'text_person_name': [
        {'confidence': 97, 'length': 4,
         'start': 1, 'text': 'UVWX'}
    ],
    'text_physical_address': [
        {'addressType': 'state', 'confidence': 97,
         'length': 3, 'start': 4, 'text': 'XYZ'}
    ]
}


def mock_annotate_note(host, note, annotator_type):
    """Get mock annotations for a note
    """
    _note = Note(
        note_type=note['note']['note_type'],
        patient_id=note['note']['patient_id'],
        text=note['note']['text'],
        identifier=note['note']['identifier']
    )
    annotation_type, annotationType = ANNOTATOR_TYPE_MAP[annotator_type]
    if _note == SAMPLE_NOTE:
        return {annotationType: SAMPLE_NOTE_ANNOTATIONS[annotation_type]}
    if _note == OVERLAPPING_NOTE:
        return {annotationType: OVERLAPPING_ANNOTATIONS[annotation_type]}
    if _note == CONFLICTING_NOTE:
        return {annotationType: CONFLICTING_ANNOTATIONS[annotation_type]}
    if _note == PARTIAL_OVERLAP_NOTE:
        return {annotationType: PARTIAL_OVERLAP_ANNOTATIONS[annotation_type]}
    raise ValueError(
        "Could not retrieve mock annotations for note: '%s'"
        % (_note,)
    )


def mock_get_tool(host):
    """Get mock annotator info
    """
    if 'person-name' in host:
        tool_type = 'nlpsandbox:person-name-annotator'
    elif 'physical-address' in host:
        tool_type = 'nlpsandbox:physical-address-annotator'
    elif 'date' in host:
        tool_type = 'nlpsandbox:date-annotator'
    else:
        tool_type = 'nlpsandbox:some-annotator-type'
    return Tool(
        name=host,
        version='1.0.0',
        license=License.APACHE_2_0,
        repository='some-user/some-repo',
        description='some tool',
        author='some person',
        author_email='someperson@somesite.org',
        url='somesite.org/some-annotator',
        tool_type=tool_type,
        tool_api_version='1.0.1'
    )
