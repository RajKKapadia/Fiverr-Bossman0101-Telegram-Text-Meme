import requests

import config


def generate_meme(text: str) -> str:
    try:
        payload = {
            "text": text
        }
        headers = {
            "Authorization": f"Bearer {config.SUPERMEME_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            "https://app.supermeme.ai/api/v1/meme/image",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        response = response.json()
        memes = response["memes"]
        return memes
    except Exception as e:
        print("Error at generate_meme ->")
        print(e)
        return []
