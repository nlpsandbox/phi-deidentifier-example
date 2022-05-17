from typing import List

from nlpsandboxclient import client

from openapi_server.models.tool import Tool  # noqa: E501
from ..config import Config
from ..models import License, ToolDependencies, ToolType, ToolDependency


def get_tool():  # noqa: E501
    """Get tool information

    Get information about the tool # noqa: E501

    :rtype: Tool
    """
    tool = Tool(
        name="phi-deidentifier",
        version="1.3.0",
        license=License.APACHE_2_0,
        repository="github:nlpsandbox/phi-deidentifier",
        description="Example implementation of the NLP Sandbox PHI "
                    "Deidentifier",
        author="NLP Sandbox Team",
        author_email="team@nlpsandbox.io",
        url="https://github.com/nlpsandbox/phi-deidentifier",
        type=ToolType.PHI_DEIDENTIFIER,
        api_version="1.2.0"
    )
    return tool, 200


def get_tool_dependencies():  # noqa: E501
    """Get tool dependencies

    Get the dependencies of this tool # noqa: E501


    :rtype: ToolDependencies
    """
    config = Config()
    tool_dependencies: List[ToolDependency] = []
    for functional_type, hostname in (
            (ToolType.DATE_ANNOTATOR, config.date_annotator_api_url),
            (ToolType.PERSON_NAME_ANNOTATOR,
             config.person_name_annotator_api_url),
            (ToolType.LOCATION_ANNOTATOR, config.location_annotator_api_url),
            (ToolType.CONTACT_ANNOTATOR, config.contact_annotator_api_url),
            (ToolType.ID_ANNOTATOR, config.id_annotator_api_url),
    ):
        client_tool = client.get_tool(host=hostname)
        tool = Tool.from_dict({client_tool.attribute_map[key]: value
                               for key, value in
                               client_tool.to_dict().items()})
        tool_dependency = ToolDependency(
            tool=tool, functional_type=functional_type)
        tool_dependencies.append(tool_dependency)
        print('ASDFEHASWEJ')
    return ToolDependencies(tool_dependencies=tool_dependencies)
