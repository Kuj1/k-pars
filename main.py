import time

import asyncio
from pyfiglet import Figlet

from scripts.get_books import main, announce_result

if __name__ == '__main__':
    title = Figlet(font='cosmic')
    print(title.renderText('K-Pars\nBooks'))
    while True:
        print('1) Start scanning data and posting')
        print('2) Start scanning data without posting')
        print('3) Show parsed results\n')
        enter_decision = int(input('Choose option and enter number:\n-> '))
        if enter_decision == 1:
            print('\n[Receiving data]\n')
            while True:
                start = time.time()
                main()
                stop = time.time()
                print(stop - start)
                asyncio.run(announce_result())
        elif enter_decision == 2:
            print('\n[Receiving data]\n')
            while True:
                start = time.time()
                main()
                stop = time.time()
                print(stop - start)
                asyncio.run(announce_result(not_to_post=True))
        elif enter_decision == 3:
            try:
                with open('result_files/result_data.txt', 'r', encoding="utf-8") as res:
                    for i in res:
                        print(i.replace('\n', ''))
            except FileNotFoundError:
                print('\n[No result yet]\n')
        else:
            print('\n[Incorrect enter value]\n')
