import datetime
import os
import json
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
another_dir_path = os.path.join(os.getcwd(), 'usefully_data')

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

first_title_hieroglyph = '만화'
second_title_hieroglyph = '웹툰'
third_title_hieroglyph = '연재'
author_hieroglyph = '그림작가'
first_publisher_hieroglyph = '네이버웹툰'
second_publisher_hieroglyph = '(<b>주식회사</b>)<b>카카오엔터테인먼트</b>'

headers = {
    'Host': 'nl.go.kr',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
    'Origin': 'https://nl.go.kr',
    'Referer': 'https://nl.go.kr/seoji/contents/S80100000000.do?topSearchType=TITLE&'
               'topSearchKeyword=%EB%84%A4%EC%9D%B4%EB%B2%84%EC%9B%B9%ED%88%B0',
    'Connection': 'close'
}

data = ['searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url'
        '%2Ckdc%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no'
        '%2Ccip_yn%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522%25EB%25A7%258C%25ED%2599%2594%2522%2520allword%2520order%2520by'
        '%2520publish_predate%2520desc%26offset%3D0%26limit%3D2000',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url%2Ckdc'
        '%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no%2Ccip_yn'
        '%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522%25EC%259B%25B9%25ED%2588%25B0%2522%2520allword%2520order%2520by'
        '%2520publish_predate%2520desc%26offset%3D0%26limit%3D2000',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url%2Ckdc'
        '%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no%2Ccip_yn'
        '%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522%25EC%2597%25B0%25EC%259E%25AC%2522%2520allword%2520order%2520by'
        '%2520publish_predate%2520desc%26offset%3D0%26limit%3D1500',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url%2Ckdc'
        '%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no%2Ccip_yn'
        '%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522%25EA%25B7%25B8%25EB%25A6%25BC%25EC%259E%2591%25EA%25B0%2580'
        '%2522%2520allword%2520order%2520by%2520publish_predate%2520desc%26offset%3D0%26limit%3D1500',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no'
        '%2Cea_isbn%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher'
        '%2Cseries_title%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date'
        '%2Cbook_size%2Cpage%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date'
        '%2Ctitle_url%2Ckdc%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url'
        '%2Ccontrol_no%2Ccip_yn%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn'
        '%2Cform_detail%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt'
        '%2Cbook_summary%26from%3Dcip.cip%26where%3Dtext_idx'
        '%253D%2522%25EB%2584%25A4%25EC%259D%25B4%25EB%25B2%2584%25EC%259B%25B9%25ED%2588%25B0%2522%2520allword'
        '%2520order%2520by%2520publish_predate%2520desc%26offset%3D0%26limit%3D2000',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url'
        '%2Ckdc%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no'
        '%2Ccip_yn%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522(%25EC%25A3%25BC%25EC%258B%259D%25ED%259A%258C%25EC%2582%25AC)'
        '%25EC%25B9%25B4%25EC%25B9%25B4%25EC%2598%25A4%25EC%2597%2594%25ED%2584%25B0%25ED%2585%258C%25EC%259D%25B8%25EB'
        '%25A8%25BC%25ED%258A%25B8%2522%2520allword%2520order%2520by%2520publish_predate%2520desc%26offset%3D0%26limit'
        '%3D500'
        ]


async def received_data(data, c) -> None:
    url = 'https://nl.go.kr/seoji/module/S80100000000_intgr_select_search_engine_data.ajax'

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False), headers=headers) as session:
        async with session.post(url, data=data) as resp:
            if resp.status != 204 and resp.headers["content-type"].strip().startswith("application/json"):
                with open(f'{os.path.join(dir_path, f"data_{c}.json")}', 'w', encoding="utf-8-sig") as outfile:
                    json.dump(await resp.json(), outfile, indent=4, ensure_ascii=False)
                print(resp.status, datetime.datetime.now())
                print(f'{resp.headers["content-type"]}\n')
            else:
                print('[Bad response]')
                print(resp.status, datetime.datetime.now())
                print(f'{resp.headers["content-type"]}\n')
        await asyncio.sleep(.25)


dt = datetime.datetime.now()
date_now = dt.strftime('%Y%m%d')
row_id = set()
with open('ids.txt', 'r', encoding="utf-8") as rowid:
    for i in rowid:
        row_id.add(i.replace('\n', ''))

counter_parse_date = 0


async def filter_result(counter: int = counter_parse_date) -> None:
    for i_dir in os.listdir(dir_path):
        try:
            with open(os.path.join(dir_path, i_dir), 'r', encoding="utf-8-sig") as doc:
                file = json.load(doc)
                try:
                    result = (x for x in file['result']['rows'])
                    for check_result in result:
                        json_res = json.dumps(check_result, indent=4, ensure_ascii=False)
                        publish_predate = check_result['fields']['publish_predate']
                        publisher = check_result['fields']['publisher']
                        author = check_result['fields']['author']
                        index_title = check_result['fields']['index_title']
                        id_res = check_result['location']['rowid']

                        url_pattern = 'https://nl.go.kr/seoji/contents/S80100000000.do?schM=intgr_detail_view_isbn&isbn='
                        set_isbn = check_result["fields"]["set_isbn"]
                        ea_isbn = check_result["fields"]["ea_isbn"]

                        if (first_title_hieroglyph in index_title) or (second_title_hieroglyph in index_title) \
                           or (third_title_hieroglyph in index_title and author_hieroglyph in author) \
                           or (first_publisher_hieroglyph in publisher) or (second_publisher_hieroglyph in publisher):

                            if (publish_predate >= date_now) and (str(id_res) not in row_id):
                                with open('ids.txt', 'a', encoding="utf-8") as ids:
                                    ids.write(f'{id_res}\n')
                                row_id.add(str(id_res))
                                link = set_isbn if set_isbn else ea_isbn
                                print(f'Title: {check_result["fields"]["title"]}\n'
                                      f'Author: {check_result["fields"]["author"]}\n'
                                      f'Publisher: {check_result["fields"]["publisher"]}\n'
                                      f'Publish_predate: {check_result["fields"]["publish_predate"]}\n'
                                      f'Link: {url_pattern}{link}\n')
                                if platform.system() == 'Windows':
                                    print('\a')
                                else:
                                    os.system("say beep")
                                await asyncio.sleep(1)

                                with open('res_data.txt', 'a', encoding="utf-8") as d:
                                    d.write(json_res + ',' + '\n')
                                counter += 1
                except KeyError:
                    continue
        except ValueError:
            continue


def get_and_output(data: str, c: int) -> None:
    asyncio.run(received_data(data, c))


def main() -> None:
    num_cores = cpu_count()

    futures = []
    length_data = len(data)

    with concurrent.futures.ProcessPoolExecutor(num_cores) as executor:
        count = 0
        for f in data:
            count += 1
            new_future = executor.submit(
                get_and_output,
                data=f,
                c=count
            )
            futures.append(new_future)
            length_data -= 1
            time.sleep(1)

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
                asyncio.run(filter_result())
        elif enter_decision == 2:
            try:
                with open('res_data.txt', 'r', encoding="utf-8") as res:
                    for i in res:
                        print(i)
            except FileNotFoundError:
                print('\n[No result yet]\n')
        else:
            print('\n[Incorrect enter value]\n')
