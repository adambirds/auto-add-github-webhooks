import json
from typing import Any, Dict

import requests


def send_completion_slack_message(config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/slack/script-complete.json", "r") as f:
        payload = json.load(f)

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["SLACK_WEBHOOK_COMPLETION"], headers=headers, data=payload
    )


def send_error_slack_message(error: str, config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/slack/script-error.json", "r") as f:
        payload = json.load(f)

    payload["blocks"][2]["fields"][0]["text"] = f"*Error:*\n{error}"

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["SLACK_WEBHOOK_ERROR"], headers=headers, data=payload
    )