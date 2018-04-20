import json
from unittest.mock import patch


def test_github_webhook_endpoint(telegram_flask_bot, flask_client):
    data = {
        "action": "opened",
        "pull_request": {
            "html_url": "https://github.com/PythonistasBR/bot/pull/43",
            "title": "Flask backend",
            "user": {"login": "fabiocerqueira"},
        },
    }
    with patch.object(telegram_flask_bot.bot, "send_message") as m:
        response = flask_client.post(
            "github/webhook", data=json.dumps(data), content_type="application/json"
        )
        m.assert_called_with(
            -123456,
            "New Pull Request from fabiocerqueira - Flask backend\n"
            "Please review it: https://github.com/PythonistasBR/bot/pull/43",
        )
    assert response.data == b"ok"


def test_github_webhook_with_empty_request(flask_client):
    response = flask_client.post("github/webhook")
    assert response.status_code == 400


def test_github_webhook_with_invalid_json(flask_client):
    data = {"action": "opened"}
    response = flask_client.post(
        "github/webhook", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 500
