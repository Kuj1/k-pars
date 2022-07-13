import datetime
import os
import platform
import concurrent.futures
import time
from multiprocessing import cpu_count

import aiohttp
import asyncio
from pyfiglet import Figlet
from bs4 import BeautifulSoup

from auto_reg import add_announce

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dir_path = os.path.join(os.getcwd(), 'processed_url')

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

dt = datetime.datetime.now()
date_now = dt.strftime('%Y-%m-%d')

headers = {
    'Host': 'nl.go.kr',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 '
                  '(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
    'Origin': 'https://nl.go.kr',
    'Connection': 'keep-alive'
}

params = [
    {
        'page': '1',
        'pageUnit': '1000',
        'schType': 'detail',
        'f1': 'title',
        'v1': '만화',
        'and1': 'AND',
        'f2': 'author',
        'and2': 'AND',
        'f3': 'publisher',
        'f5': 'isbn',
        'f7': 'kdc',
        'v8s': f'{date_now}'
    },
    {
        'page': '1',
        'pageUnit': '1000',
        'schType': 'detail',
        'f1': 'title',
        'v1': '웹툰',
        'and1': 'AND',
        'f2': 'author',
        'and2': 'AND',
        'f3': 'publisher',
        'f5': 'isbn',
        'f7': 'kdc',
        'v8s': f'{date_now}'
    },
    {
        'page': '1',
        'pageUnit': '1000',
        'schType': 'detail',
        'f1': 'title',
        'v1': '연재',
        'and1': 'AND',
        'f2': 'author',
        'v2': '그림작가',
        'and2': 'AND',
        'f3': 'publisher',
        'f5': 'isbn',
        'f7': 'kdc',
        'v8s': f'{date_now}'
    },
    {
        'page': '1',
        'pageUnit': '100',
        'schType': 'detail',
        'f3': 'publisher',
        'v3': '네이버웹툰'
    },
    {
        'page': '1',
        'pageUnit': '100',
        'schType': 'detail',
        'f3': 'publisher',
        'v3': '(주식회사)카카오엔터테인먼트'
    },

]


async def received_data(params, c) -> None:
    url = 'https://www.nl.go.kr/seoji/contents/S80100000000.do'

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False), headers=headers) as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 204 and resp.headers['Content-Type'].strip().startswith("text/html"):
                with open(f'{os.path.join(dir_path, f"data_{c}.html")}', 'w', encoding="utf-8") as outfile:
                    outfile.write(await resp.text())
                print(resp.status, datetime.datetime.now())
                print(f'{resp.headers["Content-Type"]}\n')
            else:
                print(resp.status, datetime.datetime.now())
                print(f'{resp.headers["content-type"]}\n')
        await asyncio.sleep(.25)


dt = datetime.datetime.now()
date_now = dt.strftime('%Y-%m-%d')
ref_date = dt.strftime('%Y%m%d')

url_pattern = 'https://nl.go.kr/seoji/contents/S80100000000.do?schM=intgr_detail_view_isbn&isbn='

row_id = set()
with open('ids.txt', 'r', encoding="utf-8") as rowid:
    for i in rowid:
        row_id.add(i.replace('\n', ''))

counter_parse_date = 0


async def filter_result(counter: int = counter_parse_date) -> None:
    for i_dir in os.listdir(dir_path):
        with open(os.path.join(dir_path, i_dir), 'r', encoding="utf-8") as doc:
            file = doc.read()

            soup = BeautifulSoup(file, 'lxml')
            res_data = soup.find('div', class_='resultList').find_all('div', class_='resultData')

            for check_data in res_data:
                data_block = check_data.find('div', class_='resultInfo').find('div', class_='bookData')

                title_book = str(data_block.find('div', class_='tit').find('a').get_text()).replace('\n', '')
                author_book = str(data_block.find('ul', class_='dot-list').find_all('li')[0].get_text()). \
                    replace('저자 ', ''). \
                    replace('원작자', ''). \
                    replace(' :', '')
                publisher_book = str(data_block.find('ul', class_='dot-list').find_all('li')[1].get_text()). \
                    replace('발행처: ', '')
                release_date_book = str(data_block.find('ul', class_='dot-list').find_all('li')[4].get_text()). \
                    replace('발매(예정)일:', '')
                isbn_book = str(data_block.find('ul', class_='dot-list').find_all('li')[2].get_text()). \
                    replace('ISBN: ', '').replace('세트', '').split('(')[0].replace('-', '')
                if not release_date_book.startswith(' '):
                    release_date_book = str(data_block.find('ul', class_='dot-list').find_all('li')[5].get_text()). \
                        replace('발매(예정)일:', '')
                if int(release_date_book.replace('.', '')) >= int(ref_date) and isbn_book not in row_id:
                    with open('ids.txt', 'a', encoding="utf-8") as ids:
                        ids.write(f'{isbn_book}\n')
                    row_id.add(isbn_book)

                    url_book = url_pattern + isbn_book

                    print(f'Title: {title_book}\n'
                          f'Author: {author_book}\n'
                          f'Publisher: {publisher_book}\n'
                          f'Release date: {release_date_book}\n'
                          f'Link: {url_book}\n')

                    if platform.system() == 'Windows':
                        print('\a')
                    else:
                        os.system('say beep')

                    res_books = {
                            'Title': f'{title_book}',
                            'Author': f'{author_book}',
                            'Publisher': f'{publisher_book}',
                            'Release date': f'{release_date_book}',
                            'Link': f'{url_pattern}{isbn_book}'
                        }
                    start_announce = time.time()
                    add_announce(title=title_book, link=url_book)
                    stop_announce = time.time()
                    print(stop_announce - start_announce)

                    with open('result_data.txt', 'a', encoding='utf-8') as books:
                        for key, val in res_books.items():
                            if key.startswith('Link'):
                                books.write(f'{key}:{val}\n\n')
                            else:
                                books.write(f'{key}:{val}\n')

                    await asyncio.sleep(1)
                    counter += 1


def get_and_output(params: str, c: int) -> None:
    asyncio.run(received_data(params, c))


def main() -> None:
    num_cores = cpu_count()

    futures = []
    length_data = len(params)

    with concurrent.futures.ProcessPoolExecutor(num_cores) as executor:
        count = 0
        for f in params:
            count += 1
            new_future = executor.submit(
                get_and_output,
                params=f,
                c=count
            )
            futures.append(new_future)
            length_data -= 1

    concurrent.futures.wait(futures)


if __name__ == '__main__':
    title = Figlet(font='cosmic')
    print(title.renderText('K-Pars\nBooks'))
    while True:
        print('1) Start scanning data')
        print('2) Show parsed results\n')
        enter_decision = int(input('Choose option and enter number:\n-> '))
        if enter_decision == 1:
            print('\n[Receiving data]\n')
            while True:
                start = time.time()
                main()
                stop = time.time()
                print(stop - start)
                asyncio.run(filter_result())
        elif enter_decision == 2:
            try:
                with open('result_data.txt', 'r', encoding="utf-8") as res:
                    for i in res:
                        print(i.replace('\n', ''))
            except FileNotFoundError:
                print('\n[No result yet]\n')
        else:
            print('\n[Incorrect enter value]\n')
