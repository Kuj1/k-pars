import requests
import random


def webkit():
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    webkit_number = str()

    for _ in range(16):
        symbol = random.choice(symbols)
        webkit_number += symbol

    return webkit_number


cookies = {
    'session': 'avfgnxufffj9c5nyqjzher',
    '_ym_uid': '1656756443556370607',
    '_ym_d': '1656756443',
    '_tt_enable_cookie': '1',
    '_ttp': '1c10a989-881e-4c95-a91f-e690926421f2',
    'user': '%7B%22access_token%22%3A%227LDUCtCKLR3wfqx5nWxsZ2UidMHZwQ%22%2C%22two_factor_auth%22%3Afalse%2C%22id%22%3A1109069%2C%22username%22%3A%22kontiki%22%2C%22badges%22%3A%5B%5D%2C%22is_superuser%22%3Afalse%2C%22is_staff%22%3Afalse%2C%22balance%22%3A%220.00%22%2C%22ticket_balance%22%3A0%2C%22avatar%22%3Anull%2C%22email%22%3A%22felaj%40bk.ru%22%2C%22sex%22%3A0%2C%22vk_not%22%3Afalse%2C%22yaoi%22%3A0%2C%22adult%22%3Afalse%2C%22chapters_read%22%3A0%2C%22vk_id%22%3Anull%2C%22google_id%22%3Anull%2C%22yandex_id%22%3Anull%2C%22mail_id%22%3Anull%2C%22is_two_factor_auth%22%3Afalse%2C%22tagline%22%3Anull%2C%22preference%22%3A0%2C%22count_views%22%3A0%2C%22count_votes%22%3A0%2C%22count_comments%22%3A0%7D',
    '_ga': 'GA1.2.1623638645.1656756443',
    '_ga_81J4Q19D6Y': 'GS1.1.1656839304.2.1.1656841087.0',
}

headers = {
    'Host': 'remanga.org',
    # 'Content-Length': '23920',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://remanga.org',
    'Content-Type': f'multipart/form-data; boundary=----WebKitFormBoundary{webkit}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://remanga.org/panel/add-titles/',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

files = {
    'csrfmiddlewaretoken': (None, 'fYoERkYL4BmGHl3OnrjCRz82FfAwooj2O8rSUUhJYkHcbPfwnoCf4rrW6ZCqwDo9'),
    'en_name': (None, 'Korean Marriage Ban'),
    'rus_name': (None, 'вываываывп'),
    'another_name': (None, '웹툰 금혼령-조선혼인금지령'),
    'description': (None, None),
    'type': (None, 1),
    'categories': (None, 5),
    'genres': (None, 2),
    'publishers': (None, 6122),
    'status': (None, 4),
    'age_limit': (None, 0),
    'issue_year': (None, '2022'),
    'mangachan_link': (None, None),
    'original_link': (None, 'https://eee.com/dsfd/dc111'),
    'anlate_link': (None, None),
    'cover': ('cover.png', open('cover.png', 'rb'), 'image/png'),
    'readmanga_link': (None, None),
    'user_message': (None, None)
}

response = requests.post('https://remanga.org/panel/add-titles/', cookies=cookies, files=files, verify=False)
# print(requests.Request('POST', 'https://remanga.org/panel/add-titles/', cookies=cookies, files=files).prepare().body.decode('utf8'))
print(response.text)
