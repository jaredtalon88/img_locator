# Motivation

A code challenge I came up with while walking around Fountain Painted Pots in Yellowstone after reading Mark McGrath's Python InEasySteps book.

## Setup

Use poetry to control package versions

Deploy to Cloud Run using the ./Projectfile deploy command. Change this to your own GCP Project.

## Local Development

Use dotenv to handle your Google API Key secret.

Run ./Projectfile images to build locally

Run ./Projectfile shell to get a shell inside the container

While in the shell, run ./bin/run_server to start up local dev w/ automatic uvicorn reload.

## To-Do

Unit-tests
