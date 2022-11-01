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
    loger.debug(f'ger response with requests.get({url})')
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
    return response


def change_response(url, data, directory):
    loger.debug('Change response')
    tags = get_tags_to_change(data)
    for tag in tags:
        atr, values = tag

        for val in values:
            link_to_tag = val.get(atr)
            if check_local_link(url, link_to_tag):
                full_path_to_link = urljoin(url, link_to_tag)
                path_name = get_name(url, direct=True,
                                     full_link=full_path_to_link,
                                     directory=directory)
                link_bytes = get_response(full_path_to_link)
                val[atr] = path_name

                bar = FillingSquaresBar(f'Download file to {path_name}', max=1)
                loader(os.path.join(directory, path_name),
                       link_bytes.content, bar)


def loader(path_name, link_bytes, bar):
    loger.debug(f'save content in {path_name}')
    with open(f'{path_name}', 'wb') as f:
        f.write(link_bytes)
        bar.next()
    bar.finish()
    loger.debug(f'Изображение {os.path.abspath(path_name)} успешно скачано!')
    time.sleep(randint(1, 2))


def get_tags_to_change(data) -> list:
    loger.debug('get tags to change in bs.object')
    all_tags = []
    for tag, atrrib in TAGS_FOR_DOWNLOAD.items():
        all_tags.append((atrrib, data.find_all(tag, {atrrib: True})))
    return all_tags


def check_local_link(url_1, url_2):
    loger.debug('Checking local link for base url')
    home_url_parse = urlparse(url_1).netloc
    download_url_parse = urlparse(url_2).netloc
    if home_url_parse in download_url_parse or download_url_parse == '':
        return True
    return False


def get_urlparse(path: str):
    loger.debug(f'Get urlparse from {path}')
    urlparse_result = urlparse(path.strip('/'))
    name, ext = os.path.splitext(urlparse_result.path)
    name = urlparse_result.netloc + name
    return urlparse_result, name, ext


def get_name(path, direct=None, file=None, full_link=None, directory=None):
    loger.debug('Get name')
    _, tail, ext = get_urlparse(path)
    res = ''
    for i in tail:
        if i.isdigit() or i.isalpha():
            res += i
        else:
            res += '-'
    if file:
        return res + ".html"
    if direct:
        dir_path = os.path.join(directory, res + '_files')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        name, _, ext = get_name(full_link, full_link=True)
        if not ext:
            ext = '.html'
        return f'{res}_files/{name}{ext}'
    if full_link:
        return res, tail, ext
