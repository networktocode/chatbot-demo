#!/usr/bin/env python
import requests
import json
import os
import sys
import re

from flask import Flask, request
from format_output import format_sites, format_clients, generate_template_from_j2
from helpers import read_file, build_adapative_card
from dotenv import load_dotenv

load_dotenv()

from webexteamssdk import WebexTeamsAPI, Webhook
from meraki_lib import get_site_devices, get_site_clients, get_sites


WEBEX_TEAMS_ACCESS_TOKEN = os.environ["WEBEX_TEAMS_ACCESS_TOKEN"]

flask_app = Flask(__name__)
api = WebexTeamsAPI()

def get_ip_from_str(ip_subnet):
    return re.sub('^ipcalc\s+', '' , ip_subnet)

@flask_app.route("/webex-teams/webhook/messages", methods=["POST"])
def webhook_message_listener():
    if request.method == "POST":
        json_data = request.json

        webhook_obj = Webhook(json_data)
        message = api.messages.get(webhook_obj.data.id)
        room_id = json_data["data"]["roomId"]

        # This is a VERY IMPORTANT loop prevention control step.
        bot_id = api.people.me()
        if message.personId == bot_id.id:
            return "OK"
        else:
            if "ipcalc" in message.text:
                ip_subnet = get_ip_from_str(message.text)
        
            else:
                api.messages.create(room_id, markdown="###Help:\nSyntax: ipcalc <ip_address/mask>)
            return "OK"

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
