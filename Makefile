MAKEFLAGS := --no-print-directory --silent

default: help

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\._-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

c: copy
copy: ## Copy the example-environement file
	@cp .env-example .env

venv: ## Create Local virtual environment for development and install packages
	@echo "Creating Python virtual environment and installing packages..."
	@poetry install --only api, scraper

dc: docker-compose-up
docker-compose-up: ## Start Docker Compose
	@echo "Starting Docker Compose"
	@sed 's/ENVIRONMENT=dev/ENVIRONMENT=docker/' .env > .env.tmp && \
		mv .env.tmp .env && \
		docker-compose up -d

sa: start-api
start-api: ## Start SWOOPAPI Locally
	@echo "Starting SWOOPAPI"
	@docker-compose up -d influxdb postgres
	@sed 's/ENVIRONMENT=docker/ENVIRONMENT=dev/' .env > .env.tmp && \
		mv .env.tmp .env && \
		cd api && \
		poetry run uvicorn app.main:app --host 0.0.0.0 --port 5000 --log-level debug