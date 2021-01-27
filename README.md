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

The PHI Deidentifier runs on a dockerized stack. First, make sure that you have [installed Docker](https://docs.docker.com/get-docker/)
in your local environment. Once you have done that, move your working directory to this directory, then run the
following command to start up the stack:

```
$ docker-compose up
```

When running, the Deidentifier stacks provides a web interface at [localhost:8000](http://localhost:8000) that
you can use to test out a selection of annotators on a clinical note. Currently, the deidentifier client requires
same-origin browser protection to be turned off in order to function properly. For example, Linux users with Google
Chrome can run the following command:

```bash
$ google-chrome --disable-web-security --user-data-dir=~/TEMP/
```

and then navigate to [http://localhost:8000/](http://localhost:8000/) in the newly-opened browser window.

## Development

### Server

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

### Client

The models and API hooks for the client are based on the phi-deidentifier
OpenAPI schema using
[openapi-generator-cli](https://github.com/OpenAPITools/openapi-generator-cli).
To re-generate or update these models/hooks, first download the latest
version of the API specification, then run the generator script:

```bash
$ curl -O https://nlpsandbox.github.io/nlpsandbox-schemas/phi-deidentifier/edge/openapi.yaml
$ npx openapi-generator-cli generate -g typescript-fetch -i openapi.yaml -o client/src --additional-properties=typescriptThreePlus=true
```

The client can be run locally by navigating to the `client/` directory and running `npm start`. The client depends on
the de-identifier server being run in the background. Assuming that Node and Docker are installed, the following
commands can start up the full stack (backend & frontend) for development/testing purposes using the following commands:

```bash
$ docker-compose up --build phi-deidentifier
```
(you may have to run this command as root or prepend the command with `sudo`).

Then, in another shell, run the following:

```bash
$ cd client/
$ npm start
```

The development frontend can be accessed at `http://localhost:3000`. The API calls currently require the browser to be
running with CORS enforcement disabled. This can be done with Google Chrome by, for example, running the following
command:

```bash
$ google-chrome --disable-web-security --user-data-dir=~/TEMP/
```
