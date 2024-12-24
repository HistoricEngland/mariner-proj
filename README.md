# Mariner Project - IN DEVELOPMENT

This is the top level Arches project for the Mariner system.

## Setup for development environment

CLone this into a directory called `mariner_proj`: `git clone https://github.com/HistoricEngland/mariner-proj.git mariner_proj`

This project is configured to run in a docker container development environment using the file contained in the `.ac_mariner_proj` directory.

> NOTE: This is an Arches Container CLI (ACT) configuration so can be imported to ACT and run using that.

1. clone in Arches repo and checkout dev/7.6.x

1. Compose up the `docker-compose-dependencies.yml` file. Give it a few moments to start up the database and other services.

1. Then compose up the `docker-compose.yml` file to start the Mariner project.
