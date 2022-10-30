import os
import time
from random import randint
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
import fake_useragent
import logging


def init_logger(path_to_save_log):
    # logging.basicConfig(level=logging.DEBUG)
    loger = logging.getLogger(__name__)
    FORMAT = '%(asctime)s :: %(name)s :%(lineno)s - %(levelname)s - %(message)s'
    loger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)

    fh = logging.FileHandler(filename=f'{path_to_save_log}/my_log.log')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.INFO)

    loger.addHandler(sh)
    loger.addHandler(fh)
    loger.debug('Logger was initialized')


loger = logging.getLogger(__name__)

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

TAGS_FOR_DOWNLOAD = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def download(url: str, cli_path=os.getcwd()) -> str:
    init_logger(cli_path)
    loger.info('Start func download()')
    loger.debug(f'path to creat file {cli_path}')
    # print(cli_path)
    response = get_response(url, cli_path)
    # with open('./original.html', 'w') as f:
    #     f.write(response.text)
    #     print('good')
    page_path = os.path.abspath(os.path.join(cli_path, get_name(url,
                                                                file=True)))
    # print('page_path: ', page_path)
    soup = get_bs(response.text)
    # print('3333', page_path)
    change_response(url, soup, cli_path)
    saver(soup, page_path)
    # print('page_path: ', page_path)
    # print(f'Page download sucсessfully in: {page_path}')
    loger.debug(f'Page download sucсessfully in: {page_path}')
    loger.info('Close programm')
    return page_path


def change_response(url, data, directory):
    loger.debug('Change response')
    tags = get_tags_to_change(data)
    # 'link': 'href',
    # 'script': 'src'(data)
    for tag in tags:
        atr, values = tag

        # print('fdaaa: --=-=', tag, len(values), end='\n\n')
        # print(type(tag))
        # print(atr, values)
        for val in values:
            # print('val:--- '  ,val, type(val))
            link_to_tag = val.get(atr)
            # print('link_to_tag:   ',link_to_tag)
            if check_local_link(url, link_to_tag):
                full_path_to_link = urljoin(url, link_to_tag)
                # print(full_path_to_link, ' !!!!!!!!!!!!!!@!@!!!!!!!')
                path_name = get_name(url, direct=True,
                                     full_link=full_path_to_link,
                                     directory=directory)
                # print('path_name_tp_file;   ', path_name)
                link_bytes = requests.get(full_path_to_link,
                                          timeout=1, headers=header)
                val[atr] = path_name
                loader(os.path.join(directory, path_name), link_bytes.content)


def check_scripts_for_src():
    pass


def get_tags_to_change(data) -> list:
    loger.debug('get tags to change in bs.object')
    # print('222222222222')
    # bs = get_bs(data)
    all_tags = []
    for tag, atrr in TAGS_FOR_DOWNLOAD.items():
        # print(TAGS_FOR_DOWNLOAD)
        # print(tag, val)
        all_tags.append((atrr, data.find_all(tag, {atrr: True})))
    # print('222222222222', all_tags, len(all_tags))
    return all_tags


def loader(path_name, link_bytes):
    loger.debug(f'save content in {path_name}')
    with open(f'{path_name}', 'wb') as f:
        f.write(link_bytes)

        # print(f'Изображение {os.path.abspath(path_name)} успешно скачано!')
    loger.debug(f'Изображение {os.path.abspath(path_name)} успешно скачано!')
    time.sleep(randint(1, 2))


def get_response(url, path):
    # print(path)
    loger.debug(f'ger response with requests.get({url})')
    if not os.path.exists(path):
        raise IsADirectoryError('Directory not found bla bla')
    response = requests.get(url, timeout=1, headers=header)
    response.raise_for_status()
    return response


def saver(response, path, mode='w'):
    # print(response)
    loger.debug(f'Save file in {path} with {mode}')
    with open(path, mode, encoding='utf-8') as file:
        file.write(response.prettify())


def get_bs(response):
    loger.debug('Get bs')
    return BeautifulSoup(response, 'html.parser')


def create_dir(path):
    os.mkdir(path)


def check_local_link(url_1, url_2):
    loger.debug('Checking local link for base url')
    home_url_parse = urlparse(url_1).netloc
    download_url_parse = urlparse(url_2).netloc
    # print(home_url_parse, link_to_download)
    if home_url_parse in download_url_parse or download_url_parse == '':
        # print('True')
        return True
    # print('False')
    return False


def get_urlparse(path: str):
    loger.debug(f'Get urlparse from {path}')
    urlparse_result = urlparse(path.strip('/'))
    name, ext = os.path.splitext(urlparse_result.path)
    name = urlparse_result.netloc + name
    # print('it\'s is urlparser, name and exr: ', urlparse_result, name, ext)
    return urlparse_result, name, ext


def get_name(path, direct=None, file=None, full_link=None, directory=None):
    loger.debug('Get name but im not sure:) ')
    _, tail, ext = get_urlparse(path)
    # print('parse name: ', tail)
    # print()
    res = ''
    for i in tail:
        if i.isdigit() or i.isalpha():
            res += i
        else:
            res += '-'
    # print('file name: ', res)
    if file:
        return res + ".html"
    if direct:
        try:
            # print('555556', res)
            dir_path = os.path.join(directory, res + '_files')
            create_dir(dir_path)
            # print('5555', res)
        except FileExistsError:
            loger.debug(f'Directory {dir_path} exists')
            # print(f'Directory {dir_path} exists')
        finally:
            name, _, ext = get_name(full_link, full_link=True)
            if not ext:
                ext = '.html'
                # print(f'1111111111111111 ====  {res}_files/{name}{ext}')
            return f'{res}_files/{name}{ext}'
    if full_link:
        return res, tail, ext

# pathh = os.getcwd()
# final_name = re.sub(r'\W', '-', name)#
# link2 = 'https://ru.hexlet.io/courses '
# link1 = 'https://docs.python.org/3/library/fda.txt'
# link = 'https://browser-info.ru/'


# link_2 = 'https://gas159.github.io/'
# pathh = './my_dir/'
# download(link_2, pathh)
