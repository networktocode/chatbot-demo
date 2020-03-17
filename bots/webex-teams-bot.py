#!/usr/bin/env python
import requests
import json
import os
import sys


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

help = """
### Meraki Chatbot
**WebEx Teams Chat Commands**<br>
! meraki get-arp $site-name (returns table of IP to MAC to RF)<br>
! meraki get-site $site-name (returns inventory of site devices)<br>
! meraki get-clients $site_name or $store_id (returns AP to client to signal strength)<br>
<br>
! meraki or ! meraki help - return list of supported chat commands.
"""


def get_webexteams_attachment_actions(data_id):
    url = "https://api.ciscospark.com/v1/attachment/actions/{}".format(data_id)
    headers = {
        "Authorization": "Bearer {}".format(WEBEX_TEAMS_ACCESS_TOKEN),
        "Content-Type": "application/json",
    }
    return requests.get(url, headers=headers)


def send_meraki_data_to_room(room_id, **kwargs):
    meraki_data_table = get_meraki_data(**kwargs)
    api.messages.create(
        room_id,
        text="placeholder",
        markdown="Hey, here is that data you asked about...\n```\n{}\n```".format(
            meraki_data_table
        ),
    )


def get_meraki_data(**kwargs):
    if kwargs["command"] == "get_site":
        meraki_data = get_site_devices(kwargs["site_name"])
        meraki_data_table = format_sites(meraki_data)
        return meraki_data_table
    elif kwargs["command"] == "get_clients":
        meraki_data = get_site_clients(kwargs["site_name"])
        meraki_data_table = format_clients(meraki_data)
        return meraki_data_table





@flask_app.route("/webhook/messages", methods=["POST"])
def webhook_message_listener():
    if request.method == "POST":
        json_data = request.json
        room_id = json_data["data"]["roomId"]
        webhook_obj = Webhook(json_data)
        message = api.messages.get(webhook_obj.data.id)

        # This is a VERY IMPORTANT loop prevention control step.
        bot_id = api.people.me()
        if message.personId == bot_id.id:
            return "OK"
        else:
            if "meraki get-clients" in message.text:
                meraki_sites = get_sites()
                adapative_card_json = build_adapative_card(
                    "./cards/meraki-get-clients.j2", meraki_sites
                )
                api.messages.create(
                    room_id,
                    text="meraki get-clients",
                    attachments=[adapative_card_json],
                )
            elif "meraki get-site" in message.text:
                meraki_sites = get_sites()
                adapative_card_json = build_adapative_card(
                    "./cards/meraki-get-site.j2", meraki_sites
                )
                api.messages.create(
                    room_id,
                    text="meraki get-site",
                    attachments=[adapative_card_json],
                )
            elif "meraki get-arp" in message.text:
                pass
            else:
                api.messages.create(room_id, markdown=help)
            return "OK"


@flask_app.route("/webhook/attachment_actions", methods=["POST"])
def webhook_attachment_action_listener():
    if request.method == "POST":
        json_webook_data = request.json

        # get room_id / data_id
        room_id = json_webook_data["data"]["roomId"]
        data_id = json_webook_data["data"]["id"]

        # get data input references
        attachment_data = get_webexteams_attachment_actions(data_id)

        # fetch user inputs
        json_attachment_data = json.loads(attachment_data.text)
        user_inputs = json_attachment_data["inputs"]

        send_meraki_data_to_room(room_id, **user_inputs)
        return "OK"


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5001)
