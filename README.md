# How to Build a ChatOps Bot

## Load Environment Variables
Set your environment variables by copying the example `.env` and defining your settings.
Once done run `export $(cat .env | xargs)` to export your environment variables.
```
cp .env-example .env
```

## Create Environment
Next create a virtual environment and load your Python dependancies. 
```
virtualenv --python=`which python3` venv
pip install -r requirements.txt
```

## Install System Dependancies
Install the required system dependancies via `apt-get`, or via the nesscary package manager for your distribution.
```
apt-get install ipcalc
```

## Setup Ngrok

/opt/ngrok authtoken ${NGROK_TOKEN_ENV}
/opt/ngrok http -subdomain=chatop 5030