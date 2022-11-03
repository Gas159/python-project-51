from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import fake_useragent
import requests
import logging
import os
import time
from random import randint
from page_loader.exceptions import KnownError, AllErrors
from progress.bar import FillingSquaresBar

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

TAGS_FOR_DOWNLOAD = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}
loger = logging.getLogger(__name__)


def get_bs(response):
    loger.debug('Get bs')
    return BeautifulSoup(response, 'html.parser')


def get_response(url):
    loger.debug(f'get response with requests.get({url})')
    try:
        response = requests.get(url, timeout=1, headers=header)
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        loger.error(f'An HTTP error occurred. \n{e}')
        raise KnownError() from e

    except requests.exceptions.ConnectionError as e:
        loger.error(f'A Connection error occurred.\n{e}')
        raise KnownError() from e

    except requests.exceptions.RequestException as e:
        loger.error(f'Some went wrong.\n{e}')
        raise AllErrors() from e

    else:
        return response


def change_response(url, data, directory_name):
    loger.debug('Change response')
    tags = get_tags_to_change(data)
    for tag in tags:
        atr, values = tag

        for val in values:
            link_to_tag = val.get(atr)
            if check_local_link(url, link_to_tag):
                download_link = urljoin(url, link_to_tag)

                path_to_change, path_name = generate_path(
                    url, directory_name, link_to_file=link_to_tag,
                    directory=True)
                link_bytes = get_response(download_link)
                val[atr] = path_to_change

                bar = FillingSquaresBar(f'Download file to {path_name}', max=1)
                loader(path_name, link_bytes.content, bar)


def loader(path_name, link_bytes, bar):
    loger.debug(f'save content in {path_name}')
    with open(path_name, 'wb') as f:
        f.write(link_bytes)
        bar.next()
    bar.finish()
    loger.debug(f'Изображение {os.path.abspath(path_name)} успешно скачано!')
    time.sleep(randint(1, 2))


def get_tags_to_change(data) -> list:
    loger.debug('get tags to change in bs.object')
    all_tags = []
    for tag, atr in TAGS_FOR_DOWNLOAD.items():
        all_tags.append((atr, data.find_all(tag, atr == True)))
    return all_tags


def check_local_link(url_1, url_2):
    loger.debug('Checking local link for base url')
    home_url_parse = urlparse(url_1).netloc
    download_url_parse = urlparse(url_2).netloc
    if home_url_parse is download_url_parse or download_url_parse == '':
        return True
    return False


def generate_path(url, directory_name=None, link_to_file=None, directory=None):
    urlparse_result = urlparse(url)
    costume_name = urlparse_result.netloc + urlparse_result.path
    body, ext = os.path.splitext(costume_name)
    name_of_path = generate_name(body)
    if not ext:
        ext = '.html'

    if directory:
        short_dir_name = name_of_path + '_files'
        dir_path = os.path.join(directory_name, short_dir_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        shor_file_name = generate_path(urljoin(url, link_to_file))
        file_name = os.path.join(short_dir_name, shor_file_name)
        return file_name, os.path.join(dir_path, shor_file_name)

    return name_of_path + ext


def generate_name(path):
    res = ''
    for i in path.strip('./'):
        if i.isdigit() or i.isalpha():
            res += i
        else:
            res += '-'
    return res


def check_valid_path_and_url(path_to_save_html):
    if not os.path.exists(path_to_save_html):
        loger.error(f'DirNotFound {path_to_save_html}')
        raise KnownError
