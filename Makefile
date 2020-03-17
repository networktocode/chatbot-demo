.DEFAULT_GOAL := help

DOCKER_IMG  = networktocode/chatops-demo
DOCKER_TAG  = latest
DOCKER_NAME = chatops-demo
export PYROOT=.

.PHONY: help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

### -------------------------------------------------
### FORMAT
### -------------------------------------------------

.PHONY: remove-yml-eol-spaces
remove-yml-eol-spaces: ## Remove end of line spaces from yaml files
	@echo "[*] Removing EOL YAML spaces."
	@find ./ \( -name *.yaml -o -name *.yml \) | xargs sed -i  "s/\s *$$//g"

.PHONY: black-check
black-check: ## Perform Black formatting against py files. Check ONLY.
	@echo "[*] Performing Black (Check)."
	@. ./venv/bin/activate
	@find $$PYROOT -name venv -prune -o -name '*.py' -exec black -v --check {} +

.PHONY: black-diff
black-diff: ## Perform formatting against py files. Diff ONLY.
	@echo "[*] Performing Black (Diff)."
	@. ./venv/bin/activate
	@find $$PYROOT -name venv -prune -o -name '*.py' -exec black --diff {} +

.PHONY: black
black: ## Perform formatting against py files.
	@echo "[*] Performing Black."
	@. ./venv/bin/activate
	@find $$PYROOT -name venv -prune -o -name '*.py' -exec black {} +

### -------------------------------------------------
### LINT
### -------------------------------------------------

.PHONY: pylint
lint-py: ## Perform linting against py files
	@echo "[*] Performing PyLint."
	@. ./venv/bin/activate
	@find $$PYROOT -name venv -prune -o -name '*.py' -exec pylint {} +

### -------------------------------------------------
### OTHER
### -------------------------------------------------

.PHONY: requirements
update: ## Update pip requirements.txt
	@echo "[*] Updating pip requirements.txt"
	pip freeze > requirements.txt

### -------------------------------------------------
### DOCKER
### -------------------------------------------------

build: ## build docker container.
	docker build -t $(DOCKER_IMG):$(DOCKER_TAG) .

run-detached: ## run docker container
	docker run -d -t -v $$PWD:/workspace \
	$(DOCKER_IMG):$(DOCKER_TAG)

cli: ## connect to container shell
	docker run -it -v $$PWD:/workspace \
        $(DOCKER_IMG):$(DOCKER_TAG) /bin/bash	


# :%s/^[ ]\+/\t/g - automatically replace all tabs with spaces
