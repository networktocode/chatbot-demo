.DEFAULT_GOAL := help

NGROK_TOKEN_ENV = ${NGROK_TOKEN} 

.PHONY: help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

### -------------------------------------------------
### TESTING
### -------------------------------------------------

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

# :%s/^[ ]\+/\t/g - automatically replace all tabs with spaces
