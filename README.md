```bash
 :::  .  ::::::::::. :::.    :::::::..   .::::::. 
 ;;; .;;,.`;;;```.;;;;;`;;   ;;;;``;;;; ;;;`    ` 
 [[[[[/'   `]]nnn]]',[[ '[[,  [[[,/[[[' '[==/[[[[,
_$$$$,cccc  $$$""  c$$$cc$$$c $$$$$$c     '''    $
"888"88o,   888o    888   888,888b "88bo,88b    dP
 MMM "MMP"  YMMMb   YMM   ""` MMMM   "W"  "YMmMY" 
:::::::.      ...         ...      :::  .    .::::::. 
 ;;;'';;'  .;;;;;;;.   .;;;;;;;.   ;;; .;;,.;;;`    ` 
 [[[__[[\.,[[     \[[,,[[     \[[, [[[[[/'  '[==/[[[[,
 $$""""Y$$$$$,     $$$$$$,     $$$_$$$$,      '''    $
_88o,,od8P"888,_ _,88P"888,_ _,88P"888"88o,  88b    dP
""YUMMMP"   "YMMMMMP"   "YMMMMMP"  MMM "MMP"  "YMmMY" 
```

## Перед запуском скрипта:
- Убедитесь, что установлен `Python 3.10`;
- В терминале, перейдите в директории со скриптом -> скопируйте и выполните скрипт ниже:

### Если Linux / MacOs
```bash
    virtualenv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt
```
P.S: Ни в коем случае! не удалять! `ids.txt`, на основе данных из этого файла скрипт при повторном включении не будет обрабатывать уже обработанные раннее результаты.

### Если Windows
```bash
    python -m venv env && env\Scripts\activate && pip install -r requirements.txt
```
## Описание
- Cкрипт обращается к серверу сайта корейского книжного портала и получая ответ, фильтрует его по: дате / автору / названиям.

## How to
- При запуске скрипта, появится меню выбора:
  ```bash
      1) Start scanning data
      2) Show all raw results
  ```
  Нужно выбрать и ввести цифру выбора напротив "->":
  1) Начать сканирование - запускает основной функционал скрипта;
  2) Показать "сырые" результаты - показывает все отфильтрованные результаты, которые были найдены (в том виде, в каком они пришли в ответе).
- При первом запуске, скрипт подает запросы (это может занять некотороее время, в связи с плохой пропускаемостью запросов аяксом) и получая ответы сразу обрабатывает их и выдает результаты в cli издавая при этом звук. Так же паралельно идет запись результатов в `res_data.txt`;
- После обработки полученных результатов, скрипт начинает повторно отсылать запросы и проверять ответы на наличие новых результатов. Если таковые будут, они выведутся в cli;
- При повторном включении скрипт не обрабатывает старые резльтаты, а ждет получение новых;
- Выход из скрипта осуществляется по нажатию хоткея `Ctrl-C`.
