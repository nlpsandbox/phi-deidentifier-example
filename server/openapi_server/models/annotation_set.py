# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.text_contact_annotation import TextContactAnnotation
from openapi_server.models.text_date_annotation import TextDateAnnotation
from openapi_server.models.text_id_annotation import TextIdAnnotation
from openapi_server.models.text_person_name_annotation import TextPersonNameAnnotation
from openapi_server.models.text_physical_address_annotation import TextPhysicalAddressAnnotation
from openapi_server import util

from openapi_server.models.text_contact_annotation import TextContactAnnotation  # noqa: E501
from openapi_server.models.text_date_annotation import TextDateAnnotation  # noqa: E501
from openapi_server.models.text_id_annotation import TextIdAnnotation  # noqa: E501
from openapi_server.models.text_person_name_annotation import TextPersonNameAnnotation  # noqa: E501
from openapi_server.models.text_physical_address_annotation import TextPhysicalAddressAnnotation  # noqa: E501

class AnnotationSet(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, text_date_annotations=None, text_person_name_annotations=None, text_physical_address_annotations=None, text_id_annotations=None, text_contact_annotations=None):  # noqa: E501
        """AnnotationSet - a model defined in OpenAPI

        :param text_date_annotations: The text_date_annotations of this AnnotationSet.  # noqa: E501
        :type text_date_annotations: List[TextDateAnnotation]
        :param text_person_name_annotations: The text_person_name_annotations of this AnnotationSet.  # noqa: E501
        :type text_person_name_annotations: List[TextPersonNameAnnotation]
        :param text_physical_address_annotations: The text_physical_address_annotations of this AnnotationSet.  # noqa: E501
        :type text_physical_address_annotations: List[TextPhysicalAddressAnnotation]
        :param text_id_annotations: The text_id_annotations of this AnnotationSet.  # noqa: E501
        :type text_id_annotations: List[TextIdAnnotation]
        :param text_contact_annotations: The text_contact_annotations of this AnnotationSet.  # noqa: E501
        :type text_contact_annotations: List[TextContactAnnotation]
        """
        self.openapi_types = {
            'text_date_annotations': List[TextDateAnnotation],
            'text_person_name_annotations': List[TextPersonNameAnnotation],
            'text_physical_address_annotations': List[TextPhysicalAddressAnnotation],
            'text_id_annotations': List[TextIdAnnotation],
            'text_contact_annotations': List[TextContactAnnotation]
        }

        self.attribute_map = {
            'text_date_annotations': 'textDateAnnotations',
            'text_person_name_annotations': 'textPersonNameAnnotations',
            'text_physical_address_annotations': 'textPhysicalAddressAnnotations',
            'text_id_annotations': 'textIdAnnotations',
            'text_contact_annotations': 'textContactAnnotations'
        }

        self._text_date_annotations = text_date_annotations
        self._text_person_name_annotations = text_person_name_annotations
        self._text_physical_address_annotations = text_physical_address_annotations
        self._text_id_annotations = text_id_annotations
        self._text_contact_annotations = text_contact_annotations

    @classmethod
    def from_dict(cls, dikt) -> 'AnnotationSet':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AnnotationSet of this AnnotationSet.  # noqa: E501
        :rtype: AnnotationSet
        """
        return util.deserialize_model(dikt, cls)

    @property
    def text_date_annotations(self):
        """Gets the text_date_annotations of this AnnotationSet.

        Date annotations in a text  # noqa: E501

        :return: The text_date_annotations of this AnnotationSet.
        :rtype: List[TextDateAnnotation]
        """
        return self._text_date_annotations

    @text_date_annotations.setter
    def text_date_annotations(self, text_date_annotations):
        """Sets the text_date_annotations of this AnnotationSet.

        Date annotations in a text  # noqa: E501

        :param text_date_annotations: The text_date_annotations of this AnnotationSet.
        :type text_date_annotations: List[TextDateAnnotation]
        """
        if text_date_annotations is None:
            raise ValueError("Invalid value for `text_date_annotations`, must not be `None`")  # noqa: E501

        self._text_date_annotations = text_date_annotations

    @property
    def text_person_name_annotations(self):
        """Gets the text_person_name_annotations of this AnnotationSet.

        Person name annotations in a text  # noqa: E501

        :return: The text_person_name_annotations of this AnnotationSet.
        :rtype: List[TextPersonNameAnnotation]
        """
        return self._text_person_name_annotations

    @text_person_name_annotations.setter
    def text_person_name_annotations(self, text_person_name_annotations):
        """Sets the text_person_name_annotations of this AnnotationSet.

        Person name annotations in a text  # noqa: E501

        :param text_person_name_annotations: The text_person_name_annotations of this AnnotationSet.
        :type text_person_name_annotations: List[TextPersonNameAnnotation]
        """
        if text_person_name_annotations is None:
            raise ValueError("Invalid value for `text_person_name_annotations`, must not be `None`")  # noqa: E501

        self._text_person_name_annotations = text_person_name_annotations

    @property
    def text_physical_address_annotations(self):
        """Gets the text_physical_address_annotations of this AnnotationSet.

        Physical address annotations in a text  # noqa: E501

        :return: The text_physical_address_annotations of this AnnotationSet.
        :rtype: List[TextPhysicalAddressAnnotation]
        """
        return self._text_physical_address_annotations

    @text_physical_address_annotations.setter
    def text_physical_address_annotations(self, text_physical_address_annotations):
        """Sets the text_physical_address_annotations of this AnnotationSet.

        Physical address annotations in a text  # noqa: E501

        :param text_physical_address_annotations: The text_physical_address_annotations of this AnnotationSet.
        :type text_physical_address_annotations: List[TextPhysicalAddressAnnotation]
        """
        if text_physical_address_annotations is None:
            raise ValueError("Invalid value for `text_physical_address_annotations`, must not be `None`")  # noqa: E501

        self._text_physical_address_annotations = text_physical_address_annotations

    @property
    def text_id_annotations(self):
        """Gets the text_id_annotations of this AnnotationSet.

        ID annotations in a text  # noqa: E501

        :return: The text_id_annotations of this AnnotationSet.
        :rtype: List[TextIdAnnotation]
        """
        return self._text_id_annotations

    @text_id_annotations.setter
    def text_id_annotations(self, text_id_annotations):
        """Sets the text_id_annotations of this AnnotationSet.

        ID annotations in a text  # noqa: E501

        :param text_id_annotations: The text_id_annotations of this AnnotationSet.
        :type text_id_annotations: List[TextIdAnnotation]
        """
        if text_id_annotations is None:
            raise ValueError("Invalid value for `text_id_annotations`, must not be `None`")  # noqa: E501

        self._text_id_annotations = text_id_annotations

    @property
    def text_contact_annotations(self):
        """Gets the text_contact_annotations of this AnnotationSet.

        Contact annotations in a text  # noqa: E501

        :return: The text_contact_annotations of this AnnotationSet.
        :rtype: List[TextContactAnnotation]
        """
        return self._text_contact_annotations

    @text_contact_annotations.setter
    def text_contact_annotations(self, text_contact_annotations):
        """Sets the text_contact_annotations of this AnnotationSet.

        Contact annotations in a text  # noqa: E501

        :param text_contact_annotations: The text_contact_annotations of this AnnotationSet.
        :type text_contact_annotations: List[TextContactAnnotation]
        """
        if text_contact_annotations is None:
            raise ValueError("Invalid value for `text_contact_annotations`, must not be `None`")  # noqa: E501

        self._text_contact_annotations = text_contact_annotations
