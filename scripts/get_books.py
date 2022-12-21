import datetime
import os
import platform
import concurrent.futures
import time
from multiprocessing import cpu_count

import aiohttp
import asyncio
from bs4 import BeautifulSoup

from scripts.auto_reg import add_announce

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
                # print(resp.status, datetime.datetime.now())
                # print(f'{resp.headers["Content-Type"]}\n')
            else:
                print(resp.status, datetime.datetime.now())
                print(f'{resp.headers["content-type"]}\n')
        await asyncio.sleep(.25)


ref_date = dt.strftime('%Y%m%d')

url_pattern = 'https://nl.go.kr/seoji/contents/S80100000000.do?schM=intgr_detail_view_isbn&isbn='

row_id = set()
path_to_result = os.path.join(os.getcwd(), 'result_files')
if not os.path.exists(path_to_result):
    os.mkdir(path_to_result)
    ids_file = open(os.path.join(os.getcwd(), 'result_files/ids.txt'), 'w')

path_to_ids = os.path.join(os.getcwd(), 'result_files/ids.txt')
with open(path_to_ids, 'r', encoding="utf-8") as rowid:
    for i in rowid:
        row_id.add(i.replace('\n', ''))

counter_parse_date = 0


async def announce_result(counter: int = counter_parse_date, not_to_post: bool = False) -> None:
    for i_dir in os.listdir(dir_path):
        with open(os.path.join(dir_path, i_dir), 'r', encoding="utf-8") as doc:
            file = doc.read()

            soup = BeautifulSoup(file, 'lxml')
            try:
                res_data = soup.find('div', attrs={'id': 'resultList_div'}).find_all('div', class_='resultData')

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
                        with open(path_to_ids, 'a', encoding="utf-8") as ids:
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

                        if not_to_post:
                            continue
                        else:
                            start_announce = time.time()
                            add_announce(title=title_book, link=url_book)
                            time.sleep(1)
                            stop_announce = time.time()
                            print(stop_announce - start_announce)
                            print()

                        path_to_result_data = os.path.join(os.getcwd(), 'result_files/result_data.txt')
                        with open(path_to_result_data, 'a', encoding='utf-8') as books:
                            for key, val in res_books.items():
                                if key.startswith('Link'):
                                    books.write(f'{key}:{val}\n\n')
                                else:
                                    books.write(f'{key}:{val}\n')

                        counter += 1
            except AttributeError:
                continue


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
