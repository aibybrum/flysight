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
	@docker-compose up -d

s: start
start: ## Start Jupyter Notebook Locally
	@echo "Starting Jupyter Notebook"
	@source .venv/bin/activate && \
		jupyter notebook
