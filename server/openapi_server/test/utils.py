from openapi_server.models import Note


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
        {'addressType': 'city', 'length': 7, 'start': 31, 'text': 'Seattle'}
    ]
}


def mock_get_annotations(note, annotation_type):
    if note == SAMPLE_NOTE:
        return SAMPLE_NOTE_ANNOTATIONS[annotation_type]
    else:
        raise ValueError("Could not retrieve mock annotations for note: '%s'" % (note,))
