# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.tool import Tool
from openapi_server.models.tool_type import ToolType
from openapi_server import util

from openapi_server.models.tool import Tool  # noqa: E501
from openapi_server.models.tool_type import ToolType  # noqa: E501

class ToolDependency(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, tool=None, functional_type=None):  # noqa: E501
        """ToolDependency - a model defined in OpenAPI

        :param tool: The tool of this ToolDependency.  # noqa: E501
        :type tool: Tool
        :param functional_type: The functional_type of this ToolDependency.  # noqa: E501
        :type functional_type: ToolType
        """
        self.openapi_types = {
            'tool': Tool,
            'functional_type': ToolType
        }

        self.attribute_map = {
            'tool': 'tool',
            'functional_type': 'functionalType'
        }

        self._tool = tool
        self._functional_type = functional_type

    @classmethod
    def from_dict(cls, dikt) -> 'ToolDependency':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ToolDependency of this ToolDependency.  # noqa: E501
        :rtype: ToolDependency
        """
        return util.deserialize_model(dikt, cls)

    @property
    def tool(self):
        """Gets the tool of this ToolDependency.


        :return: The tool of this ToolDependency.
        :rtype: Tool
        """
        return self._tool

    @tool.setter
    def tool(self, tool):
        """Sets the tool of this ToolDependency.


        :param tool: The tool of this ToolDependency.
        :type tool: Tool
        """
        if tool is None:
            raise ValueError("Invalid value for `tool`, must not be `None`")  # noqa: E501

        self._tool = tool

    @property
    def functional_type(self):
        """Gets the functional_type of this ToolDependency.


        :return: The functional_type of this ToolDependency.
        :rtype: ToolType
        """
        return self._functional_type

    @functional_type.setter
    def functional_type(self, functional_type):
        """Sets the functional_type of this ToolDependency.


        :param functional_type: The functional_type of this ToolDependency.
        :type functional_type: ToolType
        """
        if functional_type is None:
            raise ValueError("Invalid value for `functional_type`, must not be `None`")  # noqa: E501

        self._functional_type = functional_type
