import datetime
import os
# import json
from bs4
import platform
import concurrent.futures
import time
from multiprocessing import cpu_count

import aiohttp
import asyncio
from pyfiglet import Figlet

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dir_path = os.path.join(os.getcwd(), 'processed_url')

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

# first_title_hieroglyph = '만화' +
# second_title_hieroglyph = '웹툰' +
# third_title_hieroglyph = '연재' +
# author_hieroglyph = '그림작가' +
# first_publisher_hieroglyph = '네이버웹툰'
# second_publisher_hieroglyph = '(<b>주식회사</b>)<b>카카오엔터테인먼트</b>'

dt = datetime.datetime.now()
date_now = dt.strftime('%Y-%m-%d')

headers = {
    'Host': 'nl.go.kr',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
    'Origin': 'https://nl.go.kr',
    # 'Connection': 'close'
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
        'v3': '네이버웹툰',
        # 'v8s': f'{date_now}'
    },
    {
        'page': '1',
        'pageUnit': '100',
        'schType': 'detail',
        'f3': 'publisher',
        'v3': '(주식회사)카카오엔터테인먼트',
        # 'v8s': f'{date_now}'
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
                # print(resp.headers)
            # else:
            #     print(resp.status, datetime.datetime.now())
            #     print(f'{resp.headers["content-type"]}\n')
        await asyncio.sleep(.25)


# dt = datetime.datetime.now()
# date_now = dt.strftime('%Y%m%d')
row_id = set()
with open('ids.txt', 'r', encoding="utf-8") as rowid:
    for i in rowid:
        row_id.add(i.replace('\n', ''))

counter_parse_date = 0


# async def filter_result(counter: int = counter_parse_date) -> None:
#     for i_dir in os.listdir(dir_path):
#         try:
#             with open(os.path.join(dir_path, i_dir), 'r', encoding="utf-8-sig") as doc:
#                 file = json.load(doc)
#                 try:
#                     result = (x for x in file['result']['rows'])
#                     for check_result in result:
#                         json_res = json.dumps(check_result, indent=4, ensure_ascii=False)
#                         publish_predate = check_result['fields']['publish_predate']
#                         publisher = check_result['fields']['publisher']
#                         author = check_result['fields']['author']
#                         index_title = check_result['fields']['index_title']
#                         id_res = check_result['location']['rowid']
#
#                         url_pattern = 'https://nl.go.kr/seoji/contents/S80100000000.do?schM=intgr_detail_view_isbn&isbn='
#                         set_isbn = check_result["fields"]["set_isbn"]
#                         ea_isbn = check_result["fields"]["ea_isbn"]
#
#                         if (first_title_hieroglyph in index_title) or (second_title_hieroglyph in index_title) \
#                            or (third_title_hieroglyph in index_title and author_hieroglyph in author) \
#                            or (first_publisher_hieroglyph in publisher) or (second_publisher_hieroglyph in publisher):
#
#                             if (publish_predate >= date_now) and (str(id_res) not in row_id):
#                                 with open('ids.txt', 'a', encoding="utf-8") as ids:
#                                     ids.write(f'{id_res}\n')
#                                 row_id.add(str(id_res))
#                                 link = set_isbn if set_isbn else ea_isbn
#                                 print(f'Title: {check_result["fields"]["title"]}\n'
#                                       f'Author: {check_result["fields"]["author"]}\n'
#                                       f'Publisher: {check_result["fields"]["publisher"]}\n'
#                                       f'Publish_predate: {check_result["fields"]["publish_predate"]}\n'
#                                       f'Link: {url_pattern}{link}\n')
#                                 if platform.system() == 'Windows':
#                                     print('\a')
#                                 else:
#                                     os.system("say beep")
#                                 await asyncio.sleep(1)
#
#                                 with open('res_data.txt', 'a', encoding="utf-8") as d:
#                                     d.write(json_res + ',' + '\n')
#                                 counter += 1
#                 except KeyError:
#                     continue
#         except ValueError:
#             continue


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
            # time.sleep(2)

    concurrent.futures.wait(futures)


if __name__ == '__main__':
    title = Figlet(font='cosmic')
    print(title.renderText('K-Pars\nBooks'))
    while True:
        print('1) Start scanning data')
        print('2) Show all raw results\n')
        enter_decision = int(input('Choose option and enter number:\n-> '))
        if enter_decision == 1:
            print('\n[Receiving data]\n')
            while True:
                start = time.time()
                main()
                stop = time.time()
                print(stop - start)
                # asyncio.run(filter_result())
        elif enter_decision == 2:
            try:
                with open('res_data.txt', 'r', encoding="utf-8") as res:
                    for i in res:
                        print(i)
            except FileNotFoundError:
                print('\n[No result yet]\n')
        else:
            print('\n[Incorrect enter value]\n')
