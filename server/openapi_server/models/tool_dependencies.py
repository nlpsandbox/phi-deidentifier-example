# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.tool_dependency import ToolDependency
from openapi_server import util

from openapi_server.models.tool_dependency import ToolDependency  # noqa: E501

class ToolDependencies(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, tool_dependencies=None):  # noqa: E501
        """ToolDependencies - a model defined in OpenAPI

        :param tool_dependencies: The tool_dependencies of this ToolDependencies.  # noqa: E501
        :type tool_dependencies: List[ToolDependency]
        """
        self.openapi_types = {
            'tool_dependencies': List[ToolDependency]
        }

        self.attribute_map = {
            'tool_dependencies': 'toolDependencies'
        }

        self._tool_dependencies = tool_dependencies

    @classmethod
    def from_dict(cls, dikt) -> 'ToolDependencies':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ToolDependencies of this ToolDependencies.  # noqa: E501
        :rtype: ToolDependencies
        """
        return util.deserialize_model(dikt, cls)

    @property
    def tool_dependencies(self):
        """Gets the tool_dependencies of this ToolDependencies.

        A list of tool dependencies  # noqa: E501

        :return: The tool_dependencies of this ToolDependencies.
        :rtype: List[ToolDependency]
        """
        return self._tool_dependencies

    @tool_dependencies.setter
    def tool_dependencies(self, tool_dependencies):
        """Sets the tool_dependencies of this ToolDependencies.

        A list of tool dependencies  # noqa: E501

        :param tool_dependencies: The tool_dependencies of this ToolDependencies.
        :type tool_dependencies: List[ToolDependency]
        """
        if tool_dependencies is None:
            raise ValueError("Invalid value for `tool_dependencies`, must not be `None`")  # noqa: E501

        self._tool_dependencies = tool_dependencies
