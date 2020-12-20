# NLP Sandbox Deidentifier

[![GitHub Release](https://img.shields.io/github/release/nlpsandbox/phi-deidentifier.svg?include_prereleases&color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/phi-deidentifier/releases)
[![GitHub CI](https://img.shields.io/github/workflow/status/nlpsandbox/phi-deidentifier/ci.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/phi-deidentifier)
[![GitHub License](https://img.shields.io/github/license/nlpsandbox/phi-deidentifier.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/phi-deidentifier)
[![Docker Pulls](https://img.shields.io/docker/pulls/nlpsandbox/phi-deidentifier.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=pulls&logo=docker)](https://hub.docker.com/r/nlpsandbox/phi-deidentifier)
[![Discord](https://img.shields.io/discord/770484164393828373.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=Discord&logo=discord)](https://discord.gg/Zb4ymtF "Realtime support / chat with the community and the team")

NLP Sandbox PHI Deidentifier

## Specification

TBA

## Usage

The command below starts the Deidentifier stack locally.

    docker-compose up --build phi-deidentifier

When running, the Deidentifier stacks provides a web interface (http://localhost:3838)
that you can use to deidentify single or multiple clinical notes.

## Server

### Development

The endpoints for this server are based on the phi-deidentifier OpenAPI schema using
[openapi-generator-cli](https://github.com/OpenAPITools/openapi-generator-cli). To re-generate the server skeleton from
the latest API specification, first download the latest version of the API specification:

```
$ curl -O https://nlpsandbox.github.io/nlpsandbox-schemas/phi-deidentifier/edge/openapi.yaml
```

Then generate a skeleton server (follow the [installation
instructions](https://github.com/OpenAPITools/openapi-generator-cli#installation) for openapi-generator-cli if it is not
already installed in your local environment):

```
$ npx openapi-generator-cli generate -g python-flask -i openapi.yaml -o server
```

From there, you can install and run the generated flask server:

```
$ cd server
$ pip install -e .
$ python -m openapi_server
```


## Client

### Development

The models and API hooks for the client are based on the phi-deidentifier
OpenAPI schema using
[openapi-generator-cli](https://github.com/OpenAPITools/openapi-generator-cli).
To re-generate or update these models/hooks, first download the latest
version of the API specification, then run the generator script:

```
$ curl -O https://nlpsandbox.github.io/nlpsandbox-schemas/phi-deidentifier/edge/openapi.yaml --additional-properties=typescriptThreePlus=true
$ npx openapi-generator-cli generate -g typescript-fetch -i openapi.yaml -o client
```
