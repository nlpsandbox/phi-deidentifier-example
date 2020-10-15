# NLP Sandbox Deidentifier

<!-- [![GitHub Stars](https://img.shields.io/github/stars/Sage-Bionetworks/nlp-sandbox-deidentifier.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/Sage-Bionetworks/nlp-sandbox-deidentifier) -->
[![Docker Pulls](https://img.shields.io/docker/pulls/nlpsandbox/deidentifier-shiny-app.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=pulls&logo=docker)](https://hub.docker.com/r/Sage-Bionetworks/deidentifier-shiny-app)
[![GitHub CI](https://img.shields.io/github/workflow/status/Sage-Bionetworks/nlp-sandbox-deidentifier/ci.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/Sage-Bionetworks/nlp-sandbox-deidentifier)
[![GitHub License](https://img.shields.io/github/license/Sage-Bionetworks/nlp-sandbox-deidentifier.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/Sage-Bionetworks/nlp-sandbox-deidentifier)

NLP Sandbox de-identification client and server

## Specification

## Usage

The command below starts the Deidentifier stack locally.

    docker-compose up

When running, the Deidentifier stacks provides a web interface (http://localhost:3838)
that you can use to deidentify single or multiple clinical notes.