import threading
import time

from flask import Flask, request

from utils import generate_meme
from telegram_functions import send_message_telegram, send_photo_telegram, set_webhook_telegram

app = Flask(__name__)


@app.get("/")
def handle_home():
    return "OK", 200


def call_supermeme_api_send_message(text: str, recipient_id: str) -> None:
    send_message_telegram(
        message="Generating memes, it will take about 1 minutes...", recipient_id=recipient_id)
    urls = generate_meme(text=text)
    if len(urls) != 0:
        for i in range(len(urls)):
            if i == 3:
                break
            send_photo_telegram(
                photo_url=urls[i], recipient_id=recipient_id)
            time.sleep(1)
    else:
        send_message_telegram(
            message="Meme generation failed, please try after some time.", recipient_id=recipient_id)


@app.post("/telegram")
def handle_telegram_post():
    try:
        body = request.get_json()
        query = str(body["message"]["text"])
        recipient_id = body["message"]["from"]["id"]
        command = query.split(" ")[0]
        if command == "/start":
            send_message_telegram(
                message="Welcome! Type /meme and your prompt to generate memes.",
                recipient_id=recipient_id
            )
        else:
            prompt_words = query.split(" ")[1:]
            prompt = " ".join(prompt_words)
            threading.Thread(
                target=call_supermeme_api_send_message,
                args=(prompt, recipient_id)
            ).start()
    except:
        pass
    return "OK", 200


@app.get("/telegram")
def handle_telegram_get():
    base_url = request.base_url
    parts = base_url.split("://")[1:]
    base_url = f"""https://{"".join(parts)}"""
    flag = set_webhook_telegram(url=base_url)
    if flag:
        return "OK", 200
    else:
        return "BAD_REQUEST", 403
