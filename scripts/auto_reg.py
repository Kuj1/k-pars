import requests
import datetime
import re
import os
import base64
import json

from scripts.translator import translator


def add_announce(title, link):
    dt = datetime.datetime.now()
    year_now = dt.strftime('%Y')
    path_to_img = os.path.join(os.getcwd(), 'src/cover.png')

    nice_title = re.sub(
        r'\[웹툰]|웹툰|\(한정판\)|\(완전판\)|\[웹툰 연재]|\[웹툰판]|\[만화]|만화|\[종이책]|\[전자/코믹]|\[연재]|'
        r'\[전자출판물]|\(연재\)|\(개정판\)|\[박스세트]|\(세트\)|세트|한정판|\(완결\)|\(만화로 배우는\)|\(상\)|'
        r'\d\.|\d\d\.|\d권|\d\S\d|X{1,2}|\d|\(웹툰\)|\[개정판]|\(연재용\)|,', '', title
    ).strip()

    en_name = translator(nice_title, en=True)
    ru_name = translator(nice_title, ru=True)

    print('-' * 31, end='\n')
    print(f'Title(en): {en_name}\nTitle(ru): {ru_name}\nTitle(ko): {nice_title}')

    with open(f"{path_to_img}", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    headers = {
        'Host': 'api.remanga.org',
        # 'Content-Length': '29521',
        'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
        # 'Content-Type': 'application/json',
        'Preference': '1',
        'Sec-Ch-Ua-Mobile': '?0',
        'Authorization': 'bearer nMgOvQc9XhazaRTaaRAGsjdzgg9JSa',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Accept': '*/*',
        'Origin': 'https://remanga.org',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://remanga.org/',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    json_data = {
        'rus_name': f'{ru_name}',
        'en_name': f'{en_name}',
        'another_name': f'{nice_title}',
        'issue_year': f'{year_now}',
        'original_link': f'{link}',
        'anlate_link': '',
        'adaptation_link': '',
        'user_message': '',
        'type': 1,
        'status': 4,
        'age_limit': 0,
        'categories': [
            5,
        ],
        'genres': [
            2,
        ],
        'publishers': [
            6122,
        ],
        'cover': f'image/png;base64,{encoded_string}',
    }

    try:
        # prepare = requests.Request('POST', 'https://remanga.org/panel/add-titles/', json=json_data).prepare().body
        response = requests.post('https://api.remanga.org/api/titles/', headers=headers, data=json_data)
        # # !!! Before tests need to update auth data !!!

        # print(response.text)
        json_resp = json.loads(response.text)
        print(json_resp)

        if json_resp['msg'] == 'ok' and response.status_code != 204:
            print(f'The announcement has been added')
            print('-' * 31, end='\n')
    except Exception as ex:
        with open('error.log', 'w') as log:
            message = 'An exception of type {0} occurred.\n[ARGUMENTS]: {1!r}'.format(type(ex).__name__, ex.args)
            log.write(
                f'[ERROR]: {ex}\n[TYPE EXCEPTION]: {message}\n' + '-' * len(
                    message))
        print('The announcement was not added')
        print('-' * 31, end='\n')
