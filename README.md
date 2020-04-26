# How to Build a ChatOps Bot
This repo provides the required code, relating to the following articles, around - How to Build a ChatOps Bot.
* How to Build a Chatops Bot in WexTeams (TBC)

## Load Environment Variable
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
Download Ngrok into `/opt` via the instructions on https://dashboard.ngrok.com/get-started/setup.
Once done, set your auth token and start your Ngrok tunnel.
```
/opt/ngrok authtoken ${NGROK_TOKEN_ENV}
/opt/ngrok http -subdomain=chatop 5030
```

## Execute Chatbot
You can now start the Chatbot via:
```
python lib/webex_teams_bot.py
```