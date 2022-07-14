import requests
import os

from dotenv import load_dotenv

from scripts.get_token import get_token

load_dotenv()

IAM_TOKEN = get_token()
FOLDER_ID = os.getenv('FOLDER_ID')


def translator(title: str, en=False, ru=False) -> str:
    global target_language

    if en is True:
        target_language = 'en'
    elif ru is True:
        target_language = 'ru'

    text = title

    body = {
        "targetLanguageCode": target_language,
        "texts": text,
        "folderId": FOLDER_ID,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post(
        'https://translate.api.cloud.yandex.net/translate/v2/translate',
        json=body,
        headers=headers
    )

    out_text = response.json()['translations'][0]['text']

    return out_text