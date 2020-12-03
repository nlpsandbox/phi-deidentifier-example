# NLP Sandbox Deidentifier

[![GitHub CI](https://img.shields.io/github/workflow/status/Sage-Bionetworks/nlp-sandbox-deidentifier/ci.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/Sage-Bionetworks/nlp-sandbox-deidentifier)
[![GitHub Release](https://img.shields.io/github/release/Sage-Bionetworks/nlp-sandbox-deidentifier.svg?include_prereleases&color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/Sage-Bionetworks/nlp-sandbox-deidentifier/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/nlpsandbox/date-annotator-example.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=pulls&logo=docker)](https://hub.docker.com/r/nlpsandbox/date-annotator-example)
[![GitHub License](https://img.shields.io/github/license/Sage-Bionetworks/nlp-sandbox-deidentifier.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/Sage-Bionetworks/nlp-sandbox-deidentifier)

NLP Sandbox de-identification client and server

## Specification

TBA

## Usage

The command below starts the Deidentifier stack locally.

    docker-compose up --build deidentifier-server

When running, the Deidentifier stacks provides a web interface (http://localhost:3838)
that you can use to deidentify single or multiple clinical notes.

## Development

The endpoints for this server are based on the phi-deidentifier OpenAPI schema using
[openapi-generator-cli](https://github.com/OpenAPITools/openapi-generator-cli). To re-generate the server skeleton from
the latest API specification, first download the latest version of the API specification:

```
$ curl -O https://sage-bionetworks.github.io/nlp-sandbox-schemas/phi-deidentifier/edge/openapi.yaml
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
