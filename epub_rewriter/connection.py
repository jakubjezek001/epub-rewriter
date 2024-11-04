""" Module for communicating with LM studio server """
import requests
import json

from .constants import SERVER_URL, HEADERS


def get_server_response(data: dict) -> dict:
    """Get response from the server."""
    response = requests.post(
        SERVER_URL, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        return response.json().get("choices")[0].get("message").get("content")
    return {"error": response.text}
