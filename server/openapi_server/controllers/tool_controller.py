from nlpsandboxclient import client

from openapi_server.models.tool import Tool  # noqa: E501
from ..config import Config
from ..models import License, ToolDependencies


def get_tool():  # noqa: E501
    """Get tool information

    Get information about the tool # noqa: E501

    :rtype: Tool
    """
    tool = Tool(
        name="phi-deidentifier",
        version="1.1.0",
        license=License.APACHE_2_0,
        repository="github:nlpsandbox/phi-deidentifier",
        description="Example implementation of the NLP Sandbox PHI "
                    "Deidentifier",
        author="NLP Sandbox Team",
        author_email="team@nlpsandbox.io",
        url="https://github.com/nlpsandbox/phi-deidentifier",
        type="nlpsandbox:phi-deidentifier",
        api_version="1.2.0"
    )
    return tool, 200


def get_tool_dependencies():  # noqa: E501
    """Get tool dependencies

    Get the dependencies of this tool # noqa: E501


    :rtype: ToolDependencies
    """
    config = Config()
    tool_dependencies = []
    for hostname in (
            config.date_annotator_api_url,
            config.person_name_annotator_api_url,
            config.physical_address_annotator_api_url,
            config.contact_annotator_api_url,
            config.id_annotator_api_url,
    ):
        client_tool = client.get_tool(host=hostname)
        tool = Tool.from_dict({client_tool.attribute_map[key]: value
                               for key, value in
                               client_tool.to_dict().items()})
        tool_dependencies.append(tool)
    return ToolDependencies(tools=tool_dependencies)
