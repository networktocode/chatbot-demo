#!/usr/bin/env python
import json
import re

import requests
from dotenv import load_dotenv

from flask import Flask, request
from utilities import get_ip_from_str, ipcalc
from webexteamssdk import WebexTeamsAPI, Webhook

load_dotenv()


flask_app = Flask(__name__)

api = WebexTeamsAPI()

def is_message_from_bot(api, message):
     # IMPORTANT loop prevention control step.
    if message.personId == api.people.me():
        return True
    return False

@flask_app.route("/webex-teams/webhook", methods=["POST"])
def webhook_listener():
    if request.method == "POST":
        json_data = request.json

        webhook_obj = Webhook(json_data)
        message = api.messages.get(webhook_obj.data.id)
        #room_id = api.message.get(webhook_obj.room_id.id)
        room_id = json_data["data"]["roomId"]

        if is_message_from_bot(api, message):
            return "OK"
        else:
            if "ipcalc" in message.text:
                ip_subnet = get_ip_from_str(message.text)
                ipcalc_output = ipcalc(ip_subnet)
                api.messages.create(room_id, text=ipcalc_output)
            else:
                api.messages.create(room_id, markdown="Syntax: ipcalc <ip_address/mask>")
            return "OK"

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
