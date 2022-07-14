import requests
import os

from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv('AUTH_TOKEN')


def get_token(auth_token: str = AUTH_TOKEN, expires_time=False) -> str:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f'{{"yandexPassportOauthToken":"{AUTH_TOKEN}"}}'

    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)

    iam_token = response.json()["iamToken"]
    expires_at = str(response.json()["expiresAt"]).split('T')[1]

    if expires_time is False:
        return iam_token
    else:
        return expires_at
