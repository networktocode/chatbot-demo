import json
import re
import requests
import os
from dotenv import load_dotenv
from flask import Flask, request
from ipcalc import ipcalc
from webexteamssdk import WebexTeamsAPI


load_dotenv()

flask_app = Flask(__name__)

api = WebexTeamsAPI()


@flask_app.route("/webex-teams/webhook", methods=["POST"])
def webhook_listener():
    if request.method == "POST":
        data_id = request.json["data"]["id"]
        room_id = request.json["data"]["roomId"]

        message = api.messages.get(data_id)

        if request.json["data"]["personEmail"] == os.getenv("WEBEX_BOT_USERNAME"):
            return "OK"
        else:
            if "ipcalc" in message.text:
                subnet = re.sub("^.*ipcalc\s", "", message.text)
                ipcalc_answer = ipcalc(subnet)
                api.messages.create(
                    room_id, markdown="```\n{}\n```".format(ipcalc_answer)
                )
            return "OK"

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5030)
