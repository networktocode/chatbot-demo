.DEFAULT_GOAL := help

APP_NAME = chatbot
DOCKER_TAG = latest # TBA
NGROK_TOKEN_ENV = ${NGROK_TOKEN} 

export $(cat .env | xargs)

.PHONY: help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

#.PHONY: envar
#envar:  ## Load .env#
#	export $(cat .env | xargs)

### -------------------------------------------------
### TESTING - NOT IMPLEMENTED YET
### -------------------------------------------------

.PHONY: test
test: 	lint unit ## Perform lint, then unit testing 

.PHONY: lint
lint:  ## Perform YAML linting
	@echo "[*] Performing Lint"
	yamllint -s .
	@echo "[*] Completed Lint"

.PHONY: unit
unit: ## Perform unit tests
	@echo "[*] Performing Unit Tests"
	pytest -vvv 
	@#echo "[*] Completed Unit Tests"

### -------------------------------------------------
### PIP
### -------------------------------------------------

.PHONY: requirements
update: ## Update Pip requirements.txt
	@echo "[*] Updating pip requirements.txt"
	pip freeze > requirements.txt

### -------------------------------------------------
### NGROK
### -------------------------------------------------

.PHONY: ngrok
ngrok: ## Start ngrok tunnel
	/opt/ngrok authtoken ${NGROK_TOKEN_ENV}
	/opt/ngrok http -subdomain=chatop 5030

### -------------------------------------------------
### DOCKER
### -------------------------------------------------

.PHONY: clean
clean: ## Stop/Remove Docker container
	docker stop ${APP_NAME} ; exit 0
	docker rm ${APP_NAME} ; exit 0

.PHONY: cli
cli: ## Enter Docker container
	docker exec -it ${APP_NAME} /bin/bash

.PHONY: logs
logs: ## Enter Docker container
	docker exec -it ${APP_NAME} cat /var/log/nautobot/info.log
	@echo "=================================" 
	docker exec -it ${APP_NAME} cat /var/log/nautobot/debug.log

.PHONY: logs-t
logs-t: ## Enter Docker container
	docker exec -it ${APP_NAME} tail -f /var/log/*

.PHONY: build
build: 
	docker stop ${APP_NAME} ; exit 0
	docker rm ${APP_NAME} ; exit 0
	docker build -t ${APP_NAME} .

.PHONY: run
run: ## Run Docker container
	docker stop ${APP_NAME} ; exit 0
	docker rm ${APP_NAME} ; exit 0
	docker run -t -d \
	--name ${APP_NAME} \
	-v ~/.ssh:/root/.ssh:ro \
	-v $$PWD:/workspace \
	-p 5030:5030 \
	${APP_NAME}



# :%s/^[ ]\+/\t/g - automatically replace all tabs with spaces
