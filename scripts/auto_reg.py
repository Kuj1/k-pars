import requests
import datetime
import re
import os

from bs4 import BeautifulSoup

from scripts.translator import translator


def add_announce(title, link):
    dt = datetime.datetime.now()
    year_now = dt.strftime('%Y')
    path_to_img = os.path.join(os.getcwd(), 'src/cover.png')

    nice_title = re.sub(
        r'\[웹툰]|웹툰|\(한정판\)|\(완전판\)|\[웹툰 연재]|\[웹툰판]|\[만화]|만화|\[종이책]|\[전자/코믹]|\[연재]|'
        r'\[전자출판물]|\(연재\)|\(개정판\)|\[박스세트]|\(세트\)|세트|한정판|\(완결\)|\(만화로 배우는\)|\(상\)|\d\.|\d\d\.', '', title
    ).strip()

    en_name = translator(nice_title, en=True)
    ru_name = translator(nice_title, ru=True)

    print('-' * 31, end='\n')
    print(f'Title(en): {en_name}\nTitle(ru): {ru_name}\nTitle(ko): {nice_title}')

    cookies = {
        'session': 'avfgnxufffj9c5nyqjzher',
        '_ym_uid': '1656756443556370607',
        '_ym_d': '1656756443',
        '_tt_enable_cookie': '1',
        '_ttp': '1c10a989-881e-4c95-a91f-e690926421f2',
        '_ym_isad': '2',
        '_ym_visorc': 'b',
        '_ga': 'GA1.2.1623638645.1656756443',
        '_gid': 'GA1.2.1829334205.1657903880',
        'user': '%7B%22access_token%22%3A%22nMgOvQc9XhazaRTaaRAGsjdzgg9JSa%22'
                '%2C%22two_factor_auth%22%3Afalse%2C%22id%22%3A969647'
                '%2C%22username%22%3A%22__Kenito__%22'
                '%2C%22badges%22%3A%5B%5D%2C%22is_superuser%22'
                '%3Afalse%2C%22is_staff%22%3Afalse%2C%22balance%22'
                '%3A%220.00%22%2C%22ticket_balance%22%3A0'
                '%2C%22avatar%22%3A%22https'
                '%3A%2F%2Fstorage.yandexcloud.net%2Fmedia.remanga.org%2Fusers%2F969647%2Favatar.jpg%22%2C%22email'
                '%22%3A%22nokk7557%40gmail.com%22%2C%22sex%22%3A0%2C%22vk_not%22%3Afalse%2C%22yaoi%22'
                '%3A0%2C%22adult%22%3Afalse%2C%22chapters_read%22%3A1%2C%22vk_id%22%3Anull%2C%22google_id'
                '%22%3A%22112885013969703297020%22%2C%22yandex_id%22%3Anull%2C%22mail_id'
                '%22%3Anull%2C%22is_two_factor_auth%22%3Afalse%2C%22tagline%22%3Anull%'
                '2C%22preference%22%3A0%2C%22count_views%22%3A1%2C%22count_votes%22%3A0%2C%22count_comments%22%3A0%7D',
        '_ga_81J4Q19D6Y': 'GS1.1.1657903879.7.1.1657903920.0',
    }

    headers = {
        'Host': 'remanga.org',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://remanga.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.5060.53 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://remanga.org/panel/add-titles/',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive'
    }

    files = {
        'csrfmiddlewaretoken': (None, '1DsyPDJqxEhCuldIQJtszmkE01ESSB8Uh9gN7z3CNuo5REbv7mXRECibHJ8FiY6U'),
        'en_name': (None, f'{en_name}'),
        'rus_name': (None, f'{ru_name}'),
        'another_name': (None, f'{nice_title}'),
        'description': (None, None),
        'type': (None, 1),
        'categories': (None, 5),
        'genres': (None, 2),
        'publishers': (None, 6122),
        'status': (None, 4),
        'age_limit': (None, 0),
        'issue_year': (None, f'{year_now}'),
        'mangachan_link': (None, None),
        'original_link': (None, f'{link}'),
        'anlate_link': (None, None),
        'cover': ('cover.png', open(path_to_img, 'rb'), 'image/png'),
        'readmanga_link': (None, None),
        'user_message': (None, None)
    }

    # prepare = requests.Request('POST', 'https://remanga.org/panel/add-titles/', files=files).prepare().body
    response = requests.post('https://remanga.org/panel/add-titles/', cookies=cookies, files=files, headers=headers)
    # !!! Before tests need to update auth data !!!
    soup = BeautifulSoup(response.text, 'lxml')

    success_msg = str(soup.find('div', class_='card-body').
                      find('h1', class_='text-success text-center')).\
        replace('<h1 class="text-success text-center">', '').replace('</h1>', '').strip()

    if success_msg.startswith('Спасибо за помощь проекту') and response.status_code != 204:
        print(f'The announcement has been added')
        print('-' * 31, end='\n')
    else:
        print('The announcement was not added')
        print('-' * 31, end='\n')
