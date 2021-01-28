from openapi_server.models.tool import Tool  # noqa: E501
# from openapi_server.models.tool_dependencies import ToolDependencies  # noqa: E501


def get_tool():  # noqa: E501
    """Get tool information

    Get information about the tool # noqa: E501

    :rtype: Tool
    """
    tool = Tool(
        name="phi-deidentifier",
        version="0.3.1",
        license="apache-2.0",
        repository="github:nlpsandbox/phi-deidentifier",
        description="NLP Sandbox PHI Deidentifier",
        author="The NLP Sandbox Team",
        author_email="thomas.schaffter@sagebionetworks.org",
        url="https://github.com/nlpsandbox/phi-deidentifier",
        tool_type="nlpsandbox:phi-deidentifier"
    )
    return tool, 200


def get_tool_dependencies():  # noqa: E501
    """Get tool dependencies

    Get the dependencies of this tool # noqa: E501


    :rtype: ToolDependencies
    """
    return [], 200
