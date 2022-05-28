import datetime
import os
import json
import time
import platform

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
        '%2520publish_predate%2520desc%26offset%3D0%26limit%3D1000',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url%2Ckdc'
        '%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no%2Ccip_yn'
        '%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522%25EC%259B%25B9%25ED%2588%25B0%2522%2520allword%2520order%2520by'
        '%2520publish_predate%2520desc%26offset%3D0%26limit%3D1000',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url%2Ckdc'
        '%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no%2Ccip_yn'
        '%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522%25EC%2597%25B0%25EC%259E%25AC%2522%2520allword%2520order%2520by'
        '%2520publish_predate%2520desc%26offset%3D0%26limit%3D1000',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no%2Cea_isbn'
        '%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher%2Cseries_title'
        '%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date%2Cbook_size%2Cpage'
        '%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date%2Ctitle_url%2Ckdc'
        '%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url%2Ccontrol_no%2Ccip_yn'
        '%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn%2Cform_detail'
        '%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt%2Cbook_summary'
        '%26from%3Dcip.cip%26where%3Dtext_idx%253D%2522%25EA%25B7%25B8%25EB%25A6%25BC%25EC%259E%2591%25EA%25B0%2580'
        '%2522%2520allword%2520order%2520by%2520publish_predate%2520desc%26offset%3D0%26limit%3D150',
        'searchUrl=search%3Fselect%3Dcip_id%2Crec_key%2Ccip_key%2Cform%2Cset_expression%2Csubject%2Cseries_no'
        '%2Cea_isbn%2Cea_add_code%2Cebook_yn%2Cbib_yn%2Cset_isbn%2Cset_add_code%2Ctitle%2Cvol%2Cauthor%2Cpublisher'
        '%2Cseries_title%2Cedition_stmt%2Cpre_price%2Cpublish_year%2Cpublish_predate%2Cinput_date%2Cupdate_date'
        '%2Cbook_size%2Cpage%2Cdeposit_yn%2Creal_publish_date%2Creal_price%2Cpublisher_key%2Cimport_date%2Cchanged_date'
        '%2Ctitle_url%2Ckdc%2Cddc%2Cpublisher_url%2Cbook_introduction_url%2Cbook_summary_url%2Cbook_tb_cnt_url'
        '%2Ccontrol_no%2Ccip_yn%2Cindex_series_title%2Cindex_title%2Cindex_author%2Cindex_publisher%2Crelated_isbn'
        '%2Cform_detail%2Cform_detail_version%2Ckolis_control_no%2Ckolis_img_path%2Cbook_introduction%2Cbook_tb_cnt'
        '%2Cbook_summary%26from%3Dcip.cip%26where%3Dtext_idx'
        '%253D%2522%25EB%2584%25A4%25EC%259D%25B4%25EB%25B2%2584%25EC%259B%25B9%25ED%2588%25B0%2522%2520allword'
        '%2520order%2520by%2520publish_predate%2520desc%26offset%3D0%26limit%3D1000',
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
        '%3D1000'
        ]


async def received_data() -> None:
    url = 'https://nl.go.kr/seoji/module/S80100000000_intgr_select_search_engine_data.ajax'

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False), headers=headers) as session:
        print('Receiving data...\n')
        count_r = 0
        for i_data in data:
            count_r += 1
            async with session.post(url, data=i_data) as resp:
                with open(f'{os.path.join(dir_path, f"data_{count_r}.json")}', 'w', encoding="utf-8") as outfile:
                    json.dump(await resp.json(), outfile, indent=4, ensure_ascii=False)
        await asyncio.sleep(.25)


dt = datetime.datetime.now()
date_now = dt.strftime('%Y%m%d')
row_id = list()
with open('ids.txt', 'r', encoding="utf-8") as rowid:
    for i in rowid:
        row_id.append(i.replace('\n', ''))

counter_parse_date = 0


async def filter_result(counter: int = counter_parse_date) -> None:
    print('Analyzing data...\n')
    for i_dir in os.listdir(dir_path):
        with open(os.path.join(dir_path, i_dir), 'r', encoding="utf-8") as doc:
            file = json.load(doc)
            result = (x for x in file['result']['rows'])
            try:
                for check_result in result:
                    json_res = json.dumps(check_result, indent=4, ensure_ascii=False)
                    publish_predate = check_result['fields']['publish_predate']
                    publisher = check_result['fields']['publisher']
                    author = check_result['fields']['publisher']
                    index_title = check_result['fields']['index_title']
                    id_res = check_result['location']['rowid']
                    if (first_title_hieroglyph in index_title) or (second_title_hieroglyph in index_title) \
                        or (third_title_hieroglyph in index_title and author_hieroglyph in author) \
                        or (first_publisher_hieroglyph in publisher) or (second_publisher_hieroglyph in publisher):

                        if (publish_predate >= date_now) and (id_res not in row_id):
                            with open('ids.txt', 'a', encoding="utf-8") as ids:
                                ids.write(f'{id_res}\n')
                            row_id.append(publish_predate)
                            print(f'"title": {check_result["fields"]["title"]}\n'
                                  f'"author": {check_result["fields"]["author"]}\n'
                                  f'"publisher": {check_result["fields"]["publisher"]}\n'
                                  f'"publish_predate": {check_result["fields"]["publish_predate"]}\n'
                                  f'"pre_price": {check_result["fields"]["pre_price"]}\n'
                                  f'"set_isbn": {check_result["fields"]["publish_predate"]}\n'
                                  f'"form": {check_result["fields"]["form"]}\n')
                            print(id_res)
                            os.system("say beep")
                            await asyncio.sleep(1)

                            with open('res_data.txt', 'a', encoding="utf-8") as d:
                                d.write(json_res + ',' + '\n')
                            counter += 1
            except KeyError:
                continue


title = Figlet(font='cosmic')
print(title.renderText('K-Pars\nBooks'))

if __name__ == '__main__':
    while True:
        print('1) Start scanning data')
        print('2) Show all raw results')
        enter_decision = int(input('Choose option and enter number:\n-> '))
        if enter_decision == 1:
            while True:
                start = time.time()
                asyncio.run(received_data())
                stop = time.time()
                print(stop - start)
                asyncio.run(filter_result())
        elif enter_decision == 2:
            with open('res_data.txt', 'r', encoding="utf-8") as res:
                for i in res:
                    print(i)
