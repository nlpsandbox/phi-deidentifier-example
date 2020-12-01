# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.deidentify_request import DeidentifyRequest  # noqa: E501
from openapi_server.models.deidentify_response import DeidentifyResponse  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDeidentifiedNotesController(BaseTestCase):
    """DeidentifiedNotesController integration test stubs"""

    def test_create_deidentified_notes(self):
        """Test case for create_deidentified_notes

        Deidentify a clinical note
        """
        deidentify_request = {
  "note" : {
    "noteType" : "loinc:LP29684-5",
    "patientId" : "patientId",
    "id" : "id",
    "text" : "This is a text."
  },
  "deidentificationConfigurations" : [ {
    "deidentificationStrategy" : {
      "redactConfig" : "{}",
      "annotationTypeConfig" : "{}",
      "maskingCharConfig" : {
        "maskingChar" : "*"
      },
      "dateOffsetConfig" : {
        "offsetDays" : 0
      }
    },
    "annotationTypes" : [ "text_physical_address", "text_physical_address" ]
  }, {
    "deidentificationStrategy" : {
      "redactConfig" : "{}",
      "annotationTypeConfig" : "{}",
      "maskingCharConfig" : {
        "maskingChar" : "*"
      },
      "dateOffsetConfig" : {
        "offsetDays" : 0
      }
    },
    "annotationTypes" : [ "text_physical_address", "text_physical_address" ]
  } ]
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/deidentifiedNotes',
            method='POST',
            headers=headers,
            data=json.dumps(deidentify_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
