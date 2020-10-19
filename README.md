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

    docker-compose up

When running, the Deidentifier stacks provides a web interface (http://localhost:3838)
that you can use to deidentify single or multiple clinical notes.