from openapi_server.models.service import Service  # noqa: E501


def service():  # noqa: E501
    """Get service information

    Get information about the service # noqa: E501


    :rtype: Service
    """
    service = Service(
        name="phi-deidentifier",
        version="0.1.0",
        license="Apache-2.0",
        repository="github:nlpsandbox/phi-deidentifier",
        description="NLP Sandbox PHI-Deidentifier",
        author="The NLP Sandbox Team",
        author_email="thomas.schaffter@sagebionetworks.org",
        url="https://github.com/nlpsandbox/phi-deidentifier"
    )
    return service, 200
