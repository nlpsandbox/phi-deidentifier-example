import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.note import Note  # noqa: E501
from openapi_server import util


def deidentified_notes_read_all(note=None):  # noqa: E501
    """Get deidentified notes

    Returns the deidentified notes # noqa: E501

    :param note: 
    :type note: list | bytes

    :rtype: List[Note]
    """
    if connexion.request.is_json:
        note = [Note.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
