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


# fh = logging.FileHandler(f"{__name__}.log", mode='w')
# fh.setFormatter(logging.Formatter(
#     "%(name)s %(asctime)s %(levelname)s %(message)s"))
# fh.setLevel(logging.ERROR)
#
# loger.addHandler(fh)


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
                path_name = generate_name(url, directory_name,
                                          full_link=link_to_tag,
                                          directory=True)
                link_bytes = get_response(download_link)
                val[atr] = path_name

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


def generate_name(path, directory_name, full_link=None, directory=None, file=None):
    urlparse_result = urlparse(path.rstrip('/'))
    full_name = urlparse_result.netloc + urlparse_result.path
    only_netlock_name = urlparse_result.netloc
    # res = ''
    # for i in netloc_path_name:
    #     if i.isdigit() or i.isalpha():
    #         res += i
    #     else:
    #         res += '-'
    if file:
        return generate_path(full_name) + ".html"
    if directory:
        dir_path = os.path.join(directory_name, generate_path(full_name)  + '_files')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        print('Dir', dir_path)
        print(os.path.exists(dir_path), os.path.abspath(dir_path))

        url_result = urlparse(full_link).path
        body, ext = os.path.splitext(url_result)
        print('1111', full_link)
        print(generate_path(full_name) ,body, ext)
        print()
        if not ext:
            ext = '.html'
        if url_result[0] == '/' or url_result[0] == '.':
            file_name = generate_path(only_netlock_name) +'-' + generate_path(body) + ext
        else:
            file_name = generate_path(full_name) + '-' + generate_path(body) + ext
        print('ut us os file name', file_name)
        print()
        result = os.path.join(dir_path, file_name)
        print(type(result))

        loger.debug(f'Path name created {result}')
        return result


def generate_path(path):
    res = ''
    for i in path.strip('./'):
        if i.isdigit() or i.isalpha():
            res += i
        else:
            res += '-'
    print('Generate body', res)
    return res


# def get_name(path, direct=None, file=None, full_link=None, directory=None):
#     loger.debug('Get name')
#     _, tail, ext = get_urlparse(path)
#     res = ''
#     for i in tail:
#         if i.isdigit() or i.isalpha():
#             res += i
#         else:
#             res += '-'
#     if file:
#         return res + ".html"
#     if direct:
#         dir_path = os.path.join(directory, res + '_files')
#         if not os.path.exists(dir_path):
#             os.mkdir(dir_path)
#         name, _, ext = get_name(full_link, full_link=True)
#         if not ext:
#             ext = '.html'
#         return f'{res}_files/{name}{ext}'
#     if full_link:
#         return res, tail, ext


def check_valid_path_and_url(path_to_save_html):
    if not os.path.exists(path_to_save_html):
        loger.error(f'DirNotFound {path_to_save_html}')
        raise KnownError
