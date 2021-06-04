import os
# from abc import abstractmethod

defaultValues = {
    "SERVER_PROTOCOL": "http://",
    "SERVER_HOST": "localhost",
    "SERVER_PORT": "8080",
    "DATE_ANNOTATOR_PROTOCOL": "http://",
    "DATE_ANNOTATOR_HOST": "localhost",
    "DATE_ANNOTATOR_PORT": "9000",
    "PERSON_NAME_ANNOTATOR_PROTOCOL": "http://",
    "PERSON_NAME_ANNOTATOR_HOST": "localhost",
    "PERSON_NAME_ANNOTATOR_PORT": "9001",
    "PHYSICAL_ADDRESS_ANNOTATOR_PROTOCOL": "http://",
    "PHYSICAL_ADDRESS_ANNOTATOR_HOST": "localhost",
    "PHYSICAL_ADDRESS_ANNOTATOR_PORT": "9002",
    "CONTACT_ANNOTATOR_PROTOCOL": "http://",
    "CONTACT_ANNOTATOR_HOST": "localhost",
    "CONTACT_ANNOTATOR_PORT": "9003",
    "ID_ANNOTATOR_PROTOCOL": "http://",
    "ID_ANNOTATOR_HOST": "localhost",
    "ID_ANNOTATOR_PORT": "9004",
}


class AbstractConfig(object):
    """
    Parent Class containing get_property to return the ENV variable of default
    value if not found.
    """
    def __init__(self):
        self._defaultValues = defaultValues

    def get_property(self, property_name):
        if os.getenv(property_name) is not None:
            return os.getenv(property_name)
        # we don't want KeyError?
        if property_name not in self._defaultValues.keys():
            return None  # No default value found
        # return default value
        return self._defaultValues[property_name]


class Config(AbstractConfig):
    """
    This class is used to provide hard coded values to the application, first
    using environment variables and if not found, defaulting to those values
    provided in the defaultValues dictionary above.
    """

    @property
    def server_protocol(self):
        return self.get_property('SERVER_PROTOCOL')

    @property
    def server_host(self):
        return self.get_property('SERVER_HOST')

    @property
    def server_port(self):
        return self.get_property('SERVER_PORT')

    @property
    def server_url(self):
        return "%s%s:%s" % (
            self.server_protocol, self.server_host, self.server_port)

    @property
    def server_api_url(self):
        return '{server_url}{base_path}'.format(
            server_url=self.server_url,
            base_path='/api/v1'
        )

    @property
    def date_annotator_api_url(self):
        return '{protocol}{host}:{port}{base_path}'.format(
            protocol=self.get_property('DATE_ANNOTATOR_PROTOCOL'),
            host=self.get_property('DATE_ANNOTATOR_HOST'),
            port=self.get_property('DATE_ANNOTATOR_PORT'),
            base_path='/api/v1'
        )

    @property
    def person_name_annotator_api_url(self):
        return '{protocol}{host}:{port}{base_path}'.format(
            protocol=self.get_property('PERSON_NAME_ANNOTATOR_PROTOCOL'),
            host=self.get_property('PERSON_NAME_ANNOTATOR_HOST'),
            port=self.get_property('PERSON_NAME_ANNOTATOR_PORT'),
            base_path='/api/v1'
        )

    @property
    def physical_address_annotator_api_url(self):
        return '{protocol}{host}:{port}{base_path}'.format(
            protocol=self.get_property('PHYSICAL_ADDRESS_ANNOTATOR_PROTOCOL'),
            host=self.get_property('PHYSICAL_ADDRESS_ANNOTATOR_HOST'),
            port=self.get_property('PHYSICAL_ADDRESS_ANNOTATOR_PORT'),
            base_path='/api/v1'
        )

    @property
    def contact_annotator_api_url(self):
        return '{protocol}{host}:{port}{base_path}'.format(
            protocol=self.get_property('CONTACT_ANNOTATOR_PROTOCOL'),
            host=self.get_property('CONTACT_ANNOTATOR_HOST'),
            port=self.get_property('CONTACT_ANNOTATOR_PORT'),
            base_path='/api/v1'
        )

    @property
    def id_annotator_api_url(self):
        return '{protocol}{host}:{port}{base_path}'.format(
            protocol=self.get_property('ID_ANNOTATOR_PROTOCOL'),
            host=self.get_property('ID_ANNOTATOR_HOST'),
            port=self.get_property('ID_ANNOTATOR_PORT'),
            base_path='/api/v1'
        )
