# coding: utf-8

from __future__ import absolute_import
import unittest

import requests
from flask import json
from six import BytesIO

from openapi_server.models.deidentify_request import DeidentifyRequest  # noqa: E501
from openapi_server.models.deidentify_response import DeidentifyResponse  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


SAMPLE_NOTE = {
    "noteType": "loinc:LP29684-5",
    "patientId": "patientId",
    "text": "Mary Williamson came back from Seattle yesterday, 12 December 2013."
}


class TestDeidentifiedNotesController(BaseTestCase):
    """DeidentifiedNotesController integration test stubs"""

    def test_masking_char(self):
        """Test case for create_deidentified_notes

        Deidentify a clinical note
        """
        # Mask all fields, with different characters for each one
        masking_char_request = {
            "note": SAMPLE_NOTE,
            "deidentificationConfigurations": [
                {
                    "deidentificationStrategy": {"maskingCharConfig": {"maskingChar": "*"}},
                    "annotationTypes": ["text_physical_address"]
                },
                {
                    "deidentificationStrategy": {"maskingCharConfig": {"maskingChar": "_"}},
                    "annotationTypes": ["text_person_name"]
                },
                {
                    "deidentificationStrategy": {"maskingCharConfig": {"maskingChar": "-"}},
                    "annotationTypes": ["text_date"]
                }
            ]
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = requests.post(
            'http://127.0.0.1:9003/api/v1/deidentifiedNotes',
            headers=headers,
            data=json.dumps(masking_char_request),
        )
        self.assert200(response,
                       'Response body is : ' + response.content.decode('utf-8'))
        response_data = response.json()

        # This is what the deidentified note *should* look like (based on how we know the annotators will annotate)
        expected_deidentified_text = "____ __________ came back from ******* yesterday, 12 -------- ----."
        assert response_data['note']['text'] == expected_deidentified_text,\
            "De-identified text: '%s', should be: '%s'" % (response_data['note']['text'], expected_deidentified_text)

        # Masking char de-identification doesn't change any annotation character addresses
        assert response_data['deidentifiedAnnotations'] == response_data['originalAnnotations']


if __name__ == '__main__':
    unittest.main()
