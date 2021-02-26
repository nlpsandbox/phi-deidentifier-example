# coding: utf-8

from __future__ import absolute_import
import unittest
from unittest.mock import patch
from openapi_server.test import BaseTestCase
from openapi_server.test.utils import mock_get_tool


__doc__ = "Tests for Tool controller"


class TestToolController(BaseTestCase):
    """ToolController integration test stubs"""

    def test_get_tool(self):
        """Test case for get_tool

        Get tool information
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/tool',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @patch(
        'nlpsandboxclient.client.get_tool',
        new=mock_get_tool
    )
    def test_get_tool_dependencies(self):
        """Test case for get_tool_dependencies

        Get tool dependencies
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/tool/dependencies',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
