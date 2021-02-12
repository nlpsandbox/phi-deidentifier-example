# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.license import License
import re
from openapi_server import util

from openapi_server.models.license import License  # noqa: E501
import re  # noqa: E501

class Tool(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, version=None, license=None, repository=None, description=None, author=None, author_email=None, url=None, tool_type=None, tool_api_version=None):  # noqa: E501
        """Tool - a model defined in OpenAPI

        :param name: The name of this Tool.  # noqa: E501
        :type name: str
        :param version: The version of this Tool.  # noqa: E501
        :type version: str
        :param license: The license of this Tool.  # noqa: E501
        :type license: License
        :param repository: The repository of this Tool.  # noqa: E501
        :type repository: str
        :param description: The description of this Tool.  # noqa: E501
        :type description: str
        :param author: The author of this Tool.  # noqa: E501
        :type author: str
        :param author_email: The author_email of this Tool.  # noqa: E501
        :type author_email: str
        :param url: The url of this Tool.  # noqa: E501
        :type url: str
        :param tool_type: The tool_type of this Tool.  # noqa: E501
        :type tool_type: str
        :param tool_api_version: The tool_api_version of this Tool.  # noqa: E501
        :type tool_api_version: str
        """
        self.openapi_types = {
            'name': str,
            'version': str,
            'license': License,
            'repository': str,
            'description': str,
            'author': str,
            'author_email': str,
            'url': str,
            'tool_type': str,
            'tool_api_version': str
        }

        self.attribute_map = {
            'name': 'name',
            'version': 'version',
            'license': 'license',
            'repository': 'repository',
            'description': 'description',
            'author': 'author',
            'author_email': 'authorEmail',
            'url': 'url',
            'tool_type': 'toolType',
            'tool_api_version': 'toolApiVersion'
        }

        self._name = name
        self._version = version
        self._license = license
        self._repository = repository
        self._description = description
        self._author = author
        self._author_email = author_email
        self._url = url
        self._tool_type = tool_type
        self._tool_api_version = tool_api_version

    @classmethod
    def from_dict(cls, dikt) -> 'Tool':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Tool of this Tool.  # noqa: E501
        :rtype: Tool
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this Tool.

        The tool name  # noqa: E501

        :return: The name of this Tool.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Tool.

        The tool name  # noqa: E501

        :param name: The name of this Tool.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if name is not None and len(name) > 60:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `60`")  # noqa: E501
        if name is not None and len(name) < 3:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `3`")  # noqa: E501
        if name is not None and not re.search(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', name):  # noqa: E501
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^[a-z0-9]+(?:-[a-z0-9]+)*$/`")  # noqa: E501

        self._name = name

    @property
    def version(self):
        """Gets the version of this Tool.

        The version of the tool (SemVer string)  # noqa: E501

        :return: The version of this Tool.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Tool.

        The version of the tool (SemVer string)  # noqa: E501

        :param version: The version of this Tool.
        :type version: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501
        if version is not None and len(version) < 1:
            raise ValueError("Invalid value for `version`, length must be greater than or equal to `1`")  # noqa: E501
        if version is not None and not re.search(r'^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$', version):  # noqa: E501
            raise ValueError("Invalid value for `version`, must be a follow pattern or equal to `/^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$/`")  # noqa: E501

        self._version = version

    @property
    def license(self):
        """Gets the license of this Tool.


        :return: The license of this Tool.
        :rtype: License
        """
        return self._license

    @license.setter
    def license(self, license):
        """Sets the license of this Tool.


        :param license: The license of this Tool.
        :type license: License
        """
        if license is None:
            raise ValueError("Invalid value for `license`, must not be `None`")  # noqa: E501

        self._license = license

    @property
    def repository(self):
        """Gets the repository of this Tool.

        The place where the code lives  # noqa: E501

        :return: The repository of this Tool.
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this Tool.

        The place where the code lives  # noqa: E501

        :param repository: The repository of this Tool.
        :type repository: str
        """
        if repository is None:
            raise ValueError("Invalid value for `repository`, must not be `None`")  # noqa: E501

        self._repository = repository

    @property
    def description(self):
        """Gets the description of this Tool.

        A short, one-sentence summary of the tool  # noqa: E501

        :return: The description of this Tool.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Tool.

        A short, one-sentence summary of the tool  # noqa: E501

        :param description: The description of this Tool.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501
        if description is not None and len(description) > 100:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `100`")  # noqa: E501

        self._description = description

    @property
    def author(self):
        """Gets the author of this Tool.

        The author of the tool  # noqa: E501

        :return: The author of this Tool.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this Tool.

        The author of the tool  # noqa: E501

        :param author: The author of this Tool.
        :type author: str
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def author_email(self):
        """Gets the author_email of this Tool.

        The email address of the author  # noqa: E501

        :return: The author_email of this Tool.
        :rtype: str
        """
        return self._author_email

    @author_email.setter
    def author_email(self, author_email):
        """Sets the author_email of this Tool.

        The email address of the author  # noqa: E501

        :param author_email: The author_email of this Tool.
        :type author_email: str
        """
        if author_email is None:
            raise ValueError("Invalid value for `author_email`, must not be `None`")  # noqa: E501

        self._author_email = author_email

    @property
    def url(self):
        """Gets the url of this Tool.

        The URL to the homepage of the tool  # noqa: E501

        :return: The url of this Tool.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Tool.

        The URL to the homepage of the tool  # noqa: E501

        :param url: The url of this Tool.
        :type url: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def tool_type(self):
        """Gets the tool_type of this Tool.

        The type of this tool  # noqa: E501

        :return: The tool_type of this Tool.
        :rtype: str
        """
        return self._tool_type

    @tool_type.setter
    def tool_type(self, tool_type):
        """Sets the tool_type of this Tool.

        The type of this tool  # noqa: E501

        :param tool_type: The tool_type of this Tool.
        :type tool_type: str
        """
        if tool_type is None:
            raise ValueError("Invalid value for `tool_type`, must not be `None`")  # noqa: E501
        if tool_type is not None and len(tool_type) > 60:
            raise ValueError("Invalid value for `tool_type`, length must be less than or equal to `60`")  # noqa: E501
        if tool_type is not None and len(tool_type) < 3:
            raise ValueError("Invalid value for `tool_type`, length must be greater than or equal to `3`")  # noqa: E501
        if tool_type is not None and not re.search(r'^[a-z0-9]+(?:-[a-z0-9]+)*(:)[a-z0-9]+(?:-[a-z0-9]+)*$', tool_type):  # noqa: E501
            raise ValueError("Invalid value for `tool_type`, must be a follow pattern or equal to `/^[a-z0-9]+(?:-[a-z0-9]+)*(:)[a-z0-9]+(?:-[a-z0-9]+)*$/`")  # noqa: E501

        self._tool_type = tool_type

    @property
    def tool_api_version(self):
        """Gets the tool_api_version of this Tool.

        The version of the tool OpenAPI specification  # noqa: E501

        :return: The tool_api_version of this Tool.
        :rtype: str
        """
        return self._tool_api_version

    @tool_api_version.setter
    def tool_api_version(self, tool_api_version):
        """Sets the tool_api_version of this Tool.

        The version of the tool OpenAPI specification  # noqa: E501

        :param tool_api_version: The tool_api_version of this Tool.
        :type tool_api_version: str
        """
        if tool_api_version is None:
            raise ValueError("Invalid value for `tool_api_version`, must not be `None`")  # noqa: E501
        if tool_api_version is not None and len(tool_api_version) < 1:
            raise ValueError("Invalid value for `tool_api_version`, length must be greater than or equal to `1`")  # noqa: E501
        if tool_api_version is not None and not re.search(r'^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$', tool_api_version):  # noqa: E501
            raise ValueError("Invalid value for `tool_api_version`, must be a follow pattern or equal to `/^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$/`")  # noqa: E501

        self._tool_api_version = tool_api_version
