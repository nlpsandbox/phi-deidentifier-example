from nlpsandboxsdk.model.note import Note
from nlpsandboxsdk.model.note_id import NoteId
from nlpsandboxsdk.model.patient_id import PatientId

from openapi_server.models import Tool, License

__doc__ = "Utils and sample data for testing"


def client_note_to_request_dict(note: Note):
    """Take a (datanode) Note model object, return a JSON dict (with camelCase
    keys).
    """
    snake_note_dict = note.to_dict()
    camel_case_note_dict = {note.attribute_map[key]: value for key, value in
                            snake_note_dict.items()}
    return camel_case_note_dict


ANNOTATOR_TYPE_MAP = {
    'nlpsandbox:physical-address-nlpsandboxsdk': (
        'text_physical_address', 'textPhysicalAddressAnnotations'),
    'nlpsandbox:person-name-nlpsandboxsdk': (
        'text_person_name', 'textPersonNameAnnotations'),
    'nlpsandbox:date-nlpsandboxsdk': ('text_date', 'textDateAnnotations'),
    'nlpsandbox:contact-nlpsandboxsdk': ('text_contact', 'textContactAnnotations'),
    'nlpsandbox:id-nlpsandboxsdk': ('text_id', 'textIdAnnotations'),
}


SAMPLE_NOTE = Note(
    type="loinc:LP29684-5",
    identifier=NoteId("snote"),
    patient_id=PatientId("abc123"),
    text="Mary Williamson came back from Seattle yesterday, 12 December 2013."
)


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

EXTENDED_NOTE = Note(
    type="loinc:LP29684-5",
    identifier=NoteId("snote"),
    patient_id=PatientId("abc123"),
    text="Mary Williamson came back from Seattle yesterday, 12 December 2013. "
         "Her email is mary.williamson@gmail.com, and her SSN is 123-45-6789."
)


EXTENDED_NOTE_ANNOTATIONS = {
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
    ],
    'text_contact': [
        {'contactType': 'email', 'confidence': 95, 'length': 25, 'start': 81,
         'text': 'mary.williamson@gmail.com'}
    ],
    'text_id': [
        {'idType': 'ssn', 'confidence': 95, 'length': 11, 'start': 123,
         'text': '123-45-6789'}
    ]
}


# A note with more ambiguous PII
OVERLAPPING_NOTE = Note(
    type="loinc:LP29684-5",
    identifier=NoteId("ono"),
    patient_id=PatientId("def456"),
    text="May Williamson came back from Austin, TX yesterday, 12 June 2013."
)


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
CONFLICTING_NOTE = Note(
    type="loinc:LP29684-5",
    identifier=NoteId("cnote"),
    patient_id=PatientId("ghi789"),
    text="ABCDEFG"
)


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


PARTIAL_OVERLAP_NOTE = Note(
    type="loinc:LP29684-5",
    identifier=NoteId("ponote"),
    patient_id=PatientId("jkl123"),
    text="TUVWXYZ"
)


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


def mock_annotate_note(host, note, tool_type):
    """Get mock annotations for a note
    """
    annotation_type, annotationType = ANNOTATOR_TYPE_MAP[tool_type]
    if note == SAMPLE_NOTE:
        return {annotationType: SAMPLE_NOTE_ANNOTATIONS[annotation_type]}
    if note == EXTENDED_NOTE:
        return {annotationType: EXTENDED_NOTE_ANNOTATIONS[annotation_type]}
    if note == OVERLAPPING_NOTE:
        return {annotationType: OVERLAPPING_ANNOTATIONS[annotation_type]}
    if note == CONFLICTING_NOTE:
        return {annotationType: CONFLICTING_ANNOTATIONS[annotation_type]}
    if note == PARTIAL_OVERLAP_NOTE:
        return {annotationType: PARTIAL_OVERLAP_ANNOTATIONS[annotation_type]}
    raise ValueError(
        "Could not retrieve mock annotations for note: '%s'"
        % (note,)
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
        name='some-tool',
        version='1.0.0',
        license=License.APACHE_2_0,
        repository='some-user/some-repo',
        description='some tool',
        author='some person',
        author_email='someperson@somesite.org',
        url='somesite.org/some-annotator',
        type=tool_type,
        api_version='1.0.1'
    )
