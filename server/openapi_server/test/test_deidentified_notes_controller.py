# coding: utf-8

from __future__ import absolute_import
import unittest
from flask import json
from openapi_server.test import BaseTestCase
from openapi_server.test.utils import SAMPLE_NOTE, mock_get_annotations
from unittest.mock import patch


DEIDENTIFIER_ENDPOINT_URL = 'http://127.0.0.1:8080/api/v1/deidentifiedNotes'


class TestDeidentifiedNotesController(BaseTestCase):
    """DeidentifiedNotesController integration test stubs"""

    @patch('openapi_server.utils.annotator_client.get_annotations', new=mock_get_annotations)
    def test_masking_char(self):
        """Test case for de-identification with masking character
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

        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(masking_char_request),
            content_type='application/json'
        )
        self.assertStatus(response, 201, 'Response body is : ' + response.data.decode('utf-8'))
        response_data = response.json

        # This is what the deidentified note *should* look like (based on how we know the annotators will annotate)
        expected_deidentified_text = "____ __________ came back from ******* yesterday, -- -------- ----."
        assert response_data['deidentifiedNote']['text'] == expected_deidentified_text,\
            "De-identified text: '%s', should be: '%s'" % (response_data['deidentifiedNote']['text'], expected_deidentified_text)

        # Masking char de-identification doesn't change any annotation character addresses
        assert response_data['deidentifiedAnnotations'] == response_data['originalAnnotations']

    @patch('openapi_server.utils.annotator_client.get_annotations', new=mock_get_annotations)
    def test_redact(self):
        """Test case for de-identification with redaction
        """
        redact_request = {
            "note": SAMPLE_NOTE,
            "deidentificationConfigurations": [{
                "deidentificationStrategy": {
                    "redactConfig": {},
                },
                "annotationTypes": ["text_physical_address", "text_person_name", "text_date"]
            }]
        }

        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(redact_request),
            content_type='application/json'
        )
        self.assertStatus(response, 201, 'Response body is : ' + response.data.decode('utf-8'))
        response_data = response.json

        # This is what the deidentified note *should* look like (based on how we know the annotators will annotate)
        expected_deidentified_text = "  came back from  yesterday,   ."
        assert response_data['deidentifiedNote']['text'] == expected_deidentified_text, \
            "De-identified text: '%s', should be: '%s'" % (response_data['deidentifiedNote']['text'], expected_deidentified_text)

        # Redaction should reduce all annotation lengths to 0
        for annotation_type in ('textPersonNameAnnotations', 'textPhysicalAddressAnnotations', 'textDateAnnotations'):
            for annotation in response_data['deidentifiedAnnotations'][annotation_type]:
                assert annotation['length'] == 0, "redaction should reduce annotation length to 0, not '%s'" \
                                              % (repr(annotation),)

        all_starts = set()
        for annotation_type in ('textPersonNameAnnotations', 'textPhysicalAddressAnnotations', 'textDateAnnotations'):
            for annotation in response_data['deidentifiedAnnotations'][annotation_type]:
                # It happens to be true for the sample note that no two PHI share the same start address
                assert annotation['start'] not in all_starts, \
                    "more than one annotation should not have the same start address: '%s'" % (annotation,)
                all_starts.add(annotation['start'])
                assert 0 <= annotation['start'] < len(response_data['deidentifiedNote']['text']), \
                    "deidentified annotation outside of bounds of deidentified note: '%s'" % (annotation,)

    @patch('openapi_server.utils.annotator_client.get_annotations', new=mock_get_annotations)
    def test_annotation_type(self):
        """Test case for de-identification by replacing annotation with "[ANNOTATION_TYPE]"
        """
        annotation_type_request = {
            "note": SAMPLE_NOTE,
            "deidentificationConfigurations": [{
                "deidentificationStrategy": {
                    "annotationTypeConfig": {},
                },
                "annotationTypes": ["text_physical_address", "text_person_name", "text_date"]
            }]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(annotation_type_request),
            content_type='application/json'
        )
        self.assertStatus(response, 201, 'Response body is : ' + response.data.decode('utf-8'))
        response_data = response.json

        # Manually written based on known behavior of annotators
        expected_deidentified_text = "[TEXT_PERSON_NAME] [TEXT_PERSON_NAME] came back from [TEXT_PHYSICAL_ADDRESS] yesterday, [TEXT_DATE] [TEXT_DATE] [TEXT_DATE]."
        assert response_data['deidentifiedNote']['text'] == expected_deidentified_text

        # Get expected character address ranges of de-identified annotations
        expected_starts = [i for i in range(len(expected_deidentified_text)) if expected_deidentified_text[i] == '[']
        expected_ends = [i + 1 for i in range(len(expected_deidentified_text)) if expected_deidentified_text[i] == ']']
        expected_deidentified_annotations = list(zip(expected_starts, expected_ends))

        # Check that de-identified annotations line up
        all_annotation_lists = [response_data['deidentifiedAnnotations'][annotation_type] for annotation_type in response_data['deidentifiedAnnotations']]
        all_annotations = [item for sublist in all_annotation_lists for item in sublist]
        assert len(expected_deidentified_annotations)
        for start, end in expected_deidentified_annotations:
            length = end - start
            # Check that there is an observed annotation with matching
            assert any(annotation['start'] == start and annotation['length'] == length for annotation in all_annotations)

    @patch('openapi_server.utils.annotator_client.get_annotations', new=mock_get_annotations)
    def test_no_deid_method(self):
        """Test case for de-identification configuration with no de-identification strategy (should fail).
        """
        no_method_request = {
            "note": SAMPLE_NOTE,
            "deidentificationConfigurations": [{
                "deidentificationStrategy": {},
                "annotationTypes": ["text_physical_address", "text_person_name", "text_date"]
            }]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(no_method_request),
            content_type='application/json'
        )
        self.assertStatus(response, 400, 'Response body is : ' + response.data.decode('utf-8'))

    @patch('openapi_server.utils.annotator_client.get_annotations', new=mock_get_annotations)
    def test_multiple_strategies(self):
        """Test multiple de-identification strategies on one note.
        """
        # Note that later configurations over-ride earlier configurations
        multiple_strategies_request = {
            "note": SAMPLE_NOTE,
            "deidentificationConfigurations": [
                {
                    "deidentificationStrategy": {
                        "redactConfig": {},
                    },
                    "annotationTypes": ["text_physical_address"]
                },
                {
                    "deidentificationStrategy": {
                        "maskingCharConfig": {
                            "maskingChar": "*"
                        }
                    },
                    "annotationTypes": ["text_physical_address", "text_person_name", "text_date"]
                },
                {
                    "deidentificationStrategy": {
                        "maskingCharConfig": {
                            "maskingChar": "-"
                        }
                    },
                    "annotationTypes": ["text_person_name"]
                },
                {
                    "deidentificationStrategy": {
                        "annotationTypeConfig": {}
                    },
                    "annotationTypes": ["text_date"]
                }
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(multiple_strategies_request),
            content_type='application/json'
        )
        self.assertStatus(response, 201, 'Response body is : ' + response.data.decode('utf-8'))
        response_data = response.json

        deidentified_text = response_data['deidentifiedNote']['text']
        expected_deidentified_text = "---- ---------- came back from  yesterday, [TEXT_DATE] [TEXT_DATE] [TEXT_DATE]."
        self.assertEqual(expected_deidentified_text, deidentified_text)


if __name__ == '__main__':
    unittest.main()
