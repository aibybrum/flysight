MAKEFLAGS := --no-print-directory --silent

default: help

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\._-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

venv: venv-mac
venv-mac: ## Create Local python virtual environment for mac
	@echo "Creating Python virtual environment..."
	@python3 -m venv .venv
	@echo "Activating virtual environment..."
	@source .venv/bin/activate && \
		pip install -r env/requirements.txt

c: copy
copy: ## Copy the example-environement file
	@cp env/.env-example env/.env

dc: docker-compose-up
docker-compose-up: ## Start Docker Compose
	@echo "Starting Docker Compose"
	@sed 's/ENVIRONMENT=dev/ENVIRONMENT=docker/' env/.env > .env.tmp && \
		mv .env.tmp env/.env && \
		docker-compose up -d

sn: start-notebook
start-notebook: ## Start Jupyter Notebook Locally
	@echo "Starting Jupyter Notebook"
	@source .venv/bin/activate && \
		jupyter notebook

sa: start-api
start-api: ## Start SWOOPAPI Locally
	@echo "Starting SWOOPAPI"
	@docker-compose up -d influxdb postgres
	@sed 's/ENVIRONMENT=docker/ENVIRONMENT=dev/' env/.env > .env.tmp && \
		mv .env.tmp env/.env && \
		source .venv/bin/activate && \
		cd api && \
		uvicorn app.main:app --host 0.0.0.0 --port 5000