# NLP Sandbox Deidentifier

[![GitHub Release](https://img.shields.io/github/release/nlpsandbox/phi-deidentifier.svg?include_prereleases&color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/phi-deidentifier/releases)
[![GitHub CI](https://img.shields.io/github/workflow/status/nlpsandbox/phi-deidentifier/ci.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/phi-deidentifier)
[![GitHub License](https://img.shields.io/github/license/nlpsandbox/phi-deidentifier.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/phi-deidentifier)
[![Docker Pulls](https://img.shields.io/docker/pulls/nlpsandbox/phi-deidentifier.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=pulls&logo=docker)](https://hub.docker.com/r/nlpsandbox/phi-deidentifier)
[![Discord](https://img.shields.io/discord/770484164393828373.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=Discord&logo=discord)](https://discord.gg/Zb4ymtF "Realtime support / chat with the community and the team")

NLP Sandbox PHI Deidentifier Server

## Usage

The PHI Deidentifier runs on a dockerized stack. First, make sure that you have [installed Docker](https://docs.docker.com/get-docker/)
in your local environment. Once you have done that, move your working directory to this directory, then run the
following command to start up the stack:

```
$ docker-compose up
```

You can browse the API through a web interface at [localhost:8080/api/v1/ui](http://localhost:8080/api/v1/ui). You can
change out the back end annotators by changing the value for `image` under the `*-annotator` sections of
`docker-compose.yml`. E.g. to switch out the date annotator, change these lines:

```yaml
date-annotator:
  image: nlpsandbox/date-annotator-example:0.3.2
```

to 

```yaml
date-annotator:
  image: some-group-name/some-date-annotator:1.2.3
```

where `some-group-name` is the name of a Dockerhub organization, `some-date-annotator` is the name of a Dockerhub repo
for a date annotator, and `1.2.3` is the version tag for an image of that repo.

## Development

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
