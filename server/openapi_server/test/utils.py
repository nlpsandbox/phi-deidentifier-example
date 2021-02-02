from openapi_server.models import Note, ToolDependencies, Tool

SAMPLE_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "patientId": "patientId",
    "text": "Mary Williamson came back from Seattle yesterday, 12 December 2013."
})


SAMPLE_NOTE_ANNOTATIONS = {
    'text_date': [
        {'confidence': 95, 'dateFormat': 'YYYY', 'length': 4, 'start': 62, 'text': '2013'},
        {'confidence': 95, 'dateFormat': 'MMMM', 'length': 8, 'start': 53, 'text': 'December'},
        {'confidence': 95, 'dateFormat': 'MMMM', 'length': 2, 'start': 50, 'text': '12'}
    ],
    'text_person_name': [
        {'confidence': 95, 'length': 4, 'start': 0, 'text': 'Mary'},
        {'confidence': 95, 'length': 10, 'start': 5, 'text': 'Williamson'}
    ],
    'text_physical_address': [
        {'addressType': 'city', 'confidence': 95, 'length': 7, 'start': 31, 'text': 'Seattle'}
    ]
}


# A note with more ambiguous PII
OVERLAPPING_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "patientId": "patientId",
    "text": "May Williamson came back from Austin, TX yesterday, 12 June 2013."
})


OVERLAPPING_ANNOTATIONS = {
    'text_date': [
        {'confidence': 40, 'dateFormat': 'MM', 'length': 3, 'start': 0, 'text': 'May'},
        {'confidence': 93, 'dateFormat': 'MM', 'length': 4, 'start': 55, 'text': 'June'},
        {'confidence': 95, 'dateFormat': 'MMMM', 'length': 2, 'start': 52, 'text': '12'},
        {'confidence': 97, 'dateFormat': 'YYYY', 'length': 4, 'start': 60, 'text': '2013'}
    ],
    'text_person_name': [
        {'confidence': 55, 'length': 3, 'start': 0, 'text': 'May'},
        {'confidence': 97, 'length': 10, 'start': 4, 'text': 'Williamson'},
        {'confidence': 60, 'length': 6, 'start': 30, 'text': 'Austin'}
    ],
    'text_physical_address': [
        {'addressType': 'city', 'confidence': 30, 'length': 6, 'start': 30, 'text': 'Austin'},
        {'addressType': 'state', 'confidence': 95, 'length': 2, 'start': 38, 'text': 'TX'}
    ]
}


# A note with more ambiguous PII
CONFLICTING_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "patientId": "patientId",
    "text": "ABCDEFG"
})


CONFLICTING_ANNOTATIONS = {
    'text_date': [
        {'confidence': 97, 'dateFormat': 'MM', 'length': 3, 'start': 0, 'text': 'ABC'}
    ],
    'text_person_name': [
        {'confidence': 97, 'length': 4, 'start': 0, 'text': 'ABCD'}
    ],
    'text_physical_address': [
        {'addressType': 'state', 'confidence': 97, 'length': 5, 'start': 0, 'text': 'ABCDE'}
    ]
}


PARTIAL_OVERLAP_NOTE = Note.from_dict({
    "noteType": "loinc:LP29684-5",
    "patientId": "patientId",
    "text": "TUVWXYZ"
})


PARTIAL_OVERLAP_ANNOTATIONS = {
    'text_date': [
        {'confidence': 97, 'dateFormat': 'MM', 'length': 3, 'start': 0, 'text': 'TUV'}
    ],
    'text_person_name': [
        {'confidence': 97, 'length': 4, 'start': 1, 'text': 'UVWX'}
    ],
    'text_physical_address': [
        {'addressType': 'state', 'confidence': 97, 'length': 3, 'start': 4, 'text': 'XYZ'}
    ]
}


def mock_get_annotations(note, annotation_type):
    if note == SAMPLE_NOTE:
        return SAMPLE_NOTE_ANNOTATIONS[annotation_type]
    elif note == OVERLAPPING_NOTE:
        return OVERLAPPING_ANNOTATIONS[annotation_type]
    elif note == CONFLICTING_NOTE:
        return CONFLICTING_ANNOTATIONS[annotation_type]
    elif note == PARTIAL_OVERLAP_NOTE:
        return PARTIAL_OVERLAP_ANNOTATIONS[annotation_type]
    else:
        raise ValueError("Could not retrieve mock annotations for note: '%s'" % (note,))


def mock_get_annotators_info():
    return ToolDependencies(tool_dependencies=[])
