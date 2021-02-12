# coding: utf-8

from __future__ import absolute_import
import unittest
from unittest.mock import patch

from flask import json

from openapi_server.test import BaseTestCase
from openapi_server.test.utils import mock_get_annotations, SAMPLE_NOTE, \
    OVERLAPPING_NOTE, CONFLICTING_NOTE, PARTIAL_OVERLAP_NOTE


DEIDENTIFIER_ENDPOINT_URL = 'http://127.0.0.1:8080/api/v1/deidentifiedNotes'


class TestDeidentifiedNoteController(BaseTestCase):
    """DeidentifiedNoteController integration test stubs"""

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_masking_char(self):
        """Test case for de-identification with masking character
        """
        # Mask all fields, with different characters for each one
        masking_char_request = {
            "note": SAMPLE_NOTE,
            "deidentificationSteps": [
                {
                    "maskingCharConfig": {"maskingChar": "*"},
                    "annotationTypes": ["text_physical_address"]
                },
                {
                    "maskingCharConfig": {"maskingChar": "_"},
                    "annotationTypes": ["text_person_name"]
                },
                {
                    "maskingCharConfig": {"maskingChar": "-"},
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
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        # This is what the deidentified note *should* look like (based on how
        # we know the annotators will annotate)
        expected_deidentified_text = "____ __________ came back from *******" \
                                     " yesterday, -- -------- ----."
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

        # Masking char de-identification doesn't change any annotation
        # character addresses
        self.assertEqual(response_data['deidentifiedAnnotations'],
                         response_data['originalAnnotations'])

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_redact(self):
        """Test case for de-identification with redaction
        """
        redact_request = {
            "note": SAMPLE_NOTE,
            "deidentificationSteps": [{
                "redactConfig": {},
                "annotationTypes": ["text_physical_address",
                                    "text_person_name", "text_date"]
            }]
        }

        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(redact_request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        # This is what the deidentified note *should* look like (based on how
        # we know the annotators will annotate)
        expected_deidentified_text = "  came back from  yesterday,   ."
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

        # Redaction should reduce all annotation lengths to 0
        for annotation_type in (
                'textPersonNameAnnotations', 'textPhysicalAddressAnnotations',
                'textDateAnnotations'
        ):
            for annotation in response_data['deidentifiedAnnotations'][
                annotation_type]:
                self.assertEqual(annotation['length'], 0,
                                 "bad annotation: '%s'" % (repr(annotation),))

        all_starts = set()
        for annotation_type in ('textPersonNameAnnotations',
                                'textPhysicalAddressAnnotations',
                                'textDateAnnotations'):
            for annotation in \
                    response_data['deidentifiedAnnotations'][annotation_type]:
                # It happens to be true for the sample note that no two PHI
                # share the same start address
                self.assertNotIn(annotation['start'], all_starts)
                all_starts.add(annotation['start'])
                self.assertLessEqual(0, annotation['start'])
                self.assertLess(annotation['start'],
                                len(response_data['deidentifiedNote']['text']))

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_annotation_type(self):
        """Test case for de-identification by replacing annotation with
        "[ANNOTATION_TYPE]"
        """
        annotation_type_request = {
            "note": SAMPLE_NOTE,
            "deidentificationSteps": [{
                "annotationTypeMaskConfig": {},
                "annotationTypes": ["text_physical_address",
                                    "text_person_name", "text_date"]
            }]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(annotation_type_request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        # Manually written based on known behavior of annotators
        expected_deidentified_text = \
            "[TEXT_PERSON_NAME] [TEXT_PERSON_NAME] came back from [" \
            "TEXT_PHYSICAL_ADDRESS] yesterday, [TEXT_DATE] [TEXT_DATE] [" \
            "TEXT_DATE]."
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

        # Get expected character address ranges of de-identified annotations
        expected_starts = [i for i in range(len(expected_deidentified_text)) if
                           expected_deidentified_text[i] == '[']
        expected_ends = [i + 1 for i in range(len(expected_deidentified_text))
                         if expected_deidentified_text[i] == ']']
        expected_deidentified_annotations = list(
            zip(expected_starts, expected_ends))

        # Check that de-identified annotations line up
        all_annotation_lists = [
            response_data['deidentifiedAnnotations'][annotation_type] for
            annotation_type in response_data['deidentifiedAnnotations']]
        all_annotations = [item for sublist in all_annotation_lists for item in
                           sublist]
        self.assertEqual(len(expected_deidentified_annotations),
                         len(all_annotations))
        for start, end in expected_deidentified_annotations:
            length = end - start
            # Check that there is an observed annotation with matching
            self.assertTrue(any(
                annotation['start'] == start and annotation['length'] == length
                for annotation in all_annotations))

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_no_deid_method(self):
        """Test case for de-identification configuration with no
        de-identification strategy (should fail).
        """
        no_method_request = {
            "note": SAMPLE_NOTE,
            "deidentificationSteps": [{
                "annotationTypes": ["text_physical_address",
                                    "text_person_name", "text_date"]
            }]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(no_method_request),
            content_type='application/json'
        )
        self.assertStatus(response,
                          400, 'Response body: ' +
                          response.data.decode('utf-8'))

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_multiple_strategies(self):
        """Test multiple de-identification strategies on one note.
        """
        # Note that later configurations over-ride earlier configurations
        multiple_strategies_request = {
            "note": SAMPLE_NOTE,
            "deidentificationSteps": [
                {
                    "redactConfig": {},
                    "annotationTypes": ["text_physical_address"]
                },
                {
                    "maskingCharConfig": {
                        "maskingChar": "*"
                    },
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"]
                },
                {
                    "maskingCharConfig": {
                        "maskingChar": "-"
                    },
                    "annotationTypes": ["text_person_name"]
                },
                {
                    "annotationTypeMaskConfig": {},
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
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        deidentified_text = response_data['deidentifiedNote']['text']
        expected_deidentified_text = "---- ---------- came back from *******" \
                                     " yesterday, [TEXT_DATE] [TEXT_DATE] [" \
                                     "TEXT_DATE]."
        self.assertEqual(expected_deidentified_text, deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_type_or_mask(self):
        """Test an example multi-strategy de-identification request. Give the
        type if the confidence is above 90.0%, otherwise just mask it with "*"
        character.
        """
        type_or_mask_request = {
            "note": OVERLAPPING_NOTE,
            "deidentificationSteps": [
                {
                    "maskingCharConfig": {},  # should default to "*"
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"],
                    "confidenceThreshold": 10.0
                },
                {
                    "annotationTypeMaskConfig": {},
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"],
                    "confidenceThreshold": 90.0
                }
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(type_or_mask_request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = \
            "*** [TEXT_PERSON_NAME] came back from ******, " \
            "[TEXT_PHYSICAL_ADDRESS] yesterday, [TEXT_DATE] [TEXT_DATE] [" \
            "TEXT_DATE]."
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_mask_or_redact(self):
        """Test an example multi-strategy de-identification request. Mask if
        the confidence is above 90.0%, otherwise just redact it.
        """
        type_or_mask_request = {
            "note": OVERLAPPING_NOTE,
            "deidentificationSteps": [
                {
                    "redactConfig": {},
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"],
                    "confidenceThreshold": 10.0
                },
                {
                    "maskingCharConfig": {},
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"],
                    "confidenceThreshold": 90.0
                }
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(type_or_mask_request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = \
            " ********** came back from , ** yesterday, ** **** ****."
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_redact_over_confidence(self):
        type_or_mask_request = {
            "note": OVERLAPPING_NOTE,
            "deidentificationSteps": [
                {
                    "redactConfig": {},
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"],
                    "confidenceThreshold": 90.0
                },
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(type_or_mask_request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = \
            "May  came back from Austin,  yesterday,   ."
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_conflicting_masks(self):
        """Test for the weird edge behavior that happens when annotations of
        different types partially overlap
        """
        request = {
            "note": CONFLICTING_NOTE,
            "deidentificationSteps": [
                {
                    "maskingCharConfig": {
                        "maskingChar": "*"
                    },
                    "annotationTypes": ["text_date"],
                    "confidenceThreshold": 90.0
                },
                {
                    "maskingCharConfig": {
                        "maskingChar": "-"
                    },
                    "annotationTypes": ["text_person_name"],
                    "confidenceThreshold": 90.0
                },
                {
                    "maskingCharConfig": {
                        "maskingChar": "_"
                    },
                    "annotationTypes": ["text_physical_address"],
                    "confidenceThreshold": 90.0
                },
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = "_____FG"
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_conflicting_masks_reverse(self):
        """Reverse order of masking compared to test_conflicting_masks()
        """
        request = {
            "note": CONFLICTING_NOTE,
            "deidentificationSteps": [
                {
                    "maskingCharConfig": {
                        "maskingChar": "_"
                    },
                    "annotationTypes": ["text_physical_address"],
                    "confidenceThreshold": 90.0
                },
                {
                    "maskingCharConfig": {
                        "maskingChar": "-"
                    },
                    "annotationTypes": ["text_person_name"],
                    "confidenceThreshold": 90.0
                },
                {
                    "maskingCharConfig": {
                        "maskingChar": "*"
                    },
                    "annotationTypes": ["text_date"],
                    "confidenceThreshold": 90.0
                },
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = "***----_____FG"
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_conflicting_annotation_types(self):
        request = {
            "note": CONFLICTING_NOTE,
            "deidentificationSteps": [
                {
                    "annotationTypeMaskConfig": {},
                    "annotationTypes": ["text_date", "text_person_name",
                                        "text_physical_address"],
                    "confidenceThreshold": 90.0
                },
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = "[TEXT_PHYSICAL_ADDRESS]FG"
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_conflicting_annotation_types_reverse(self):
        request = {
            "note": CONFLICTING_NOTE,
            "deidentificationSteps": [
                {
                    "annotationTypeMaskConfig": {},
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"],
                    "confidenceThreshold": 90.0
                },
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = \
            "[TEXT_DATE][TEXT_PERSON_NAME][TEXT_PHYSICAL_ADDRESS]FG"
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_partial_overlap_mask(self):
        request = {
            "note": PARTIAL_OVERLAP_NOTE,
            "deidentificationSteps": [
                {
                    "maskingCharConfig": {"maskingChar": "*"},
                    "annotationTypes": ["text_physical_address"]
                },
                {
                    "maskingCharConfig": {"maskingChar": "_"},
                    "annotationTypes": ["text_person_name"]
                },
                {
                    "maskingCharConfig": {"maskingChar": "-"},
                    "annotationTypes": ["text_date"]
                }
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = "---____***"
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_partial_overlap_mask_reverse(self):
        request = {
            "note": PARTIAL_OVERLAP_NOTE,
            "deidentificationSteps": [
                {
                    "maskingCharConfig": {"maskingChar": "-"},
                    "annotationTypes": ["text_date"]
                },
                {
                    "maskingCharConfig": {"maskingChar": "_"},
                    "annotationTypes": ["text_person_name"]
                },
                {
                    "maskingCharConfig": {"maskingChar": "*"},
                    "annotationTypes": ["text_physical_address"]
                }
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        # FIXME: The behavior being tested for here is arguably a bug due to
        #        the fact that it is erasing certain annotations that partially
        #        overlap with one another.
        expected_deidentified_text = "***"
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_partial_overlap_annotation_type(self):
        request = {
            "note": PARTIAL_OVERLAP_NOTE,
            "deidentificationSteps": [
                {
                    "annotationTypeMaskConfig": {},
                    "annotationTypes": ["text_physical_address",
                                        "text_person_name", "text_date"]
                }
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        expected_deidentified_text = \
            "[TEXT_DATE][TEXT_PERSON_NAME][TEXT_PHYSICAL_ADDRESS]"
        self.assertEqual(response_data['deidentifiedNote']['text'],
                         expected_deidentified_text)

    @patch('openapi_server.phi_deidentifier.annotators.annotate',
           new=mock_get_annotations)
    def test_partial_overlap_annotation_type_reverse(self):
        request = {
            "note": PARTIAL_OVERLAP_NOTE,
            "deidentificationSteps": [
                {
                    "annotationTypeMaskConfig": {},
                    "annotationTypes": ["text_date", "text_person_name",
                                        "text_physical_address"]
                }
            ]
        }
        response = self.client.open(
            DEIDENTIFIER_ENDPOINT_URL,
            method='POST',
            headers={'Accept': 'application/json'},
            data=json.dumps(request),
            content_type='application/json'
        )
        self.assertStatus(response, 200,
                          'Response body:' + response.data.decode('utf-8'))
        response_data = response.json

        # FIXME: This is another (arguable, see FIXME in
        #        test_partial_overlap_mask_reverse) bug from handling
        #        partially-overlapping annotations.
        expected_deidentified_text = "[TEXT_PHYSICAL_ADDRESS]"
        self.assertEqual(
            response_data['deidentifiedNote']['text'],
            expected_deidentified_text
        )


if __name__ == '__main__':
    unittest.main()
