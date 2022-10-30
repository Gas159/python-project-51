import os
import time
from random import randint
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
import fake_useragent

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
    print(cli_path)
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
    print(f'Page download sucсessfully in: {page_path}')
    return page_path


def change_response(url, data, dir):
    tags = get_tags_to_change(data)
    # 'link': 'href',
    # 'script': 'src'(data)
    for tag in tags:
        atr, values = tag

        print('fdaaa: --=-=', tag, len(values), end='\n\n')
        # print(type(tag))
        # print(atr, values)
        for val in values:
            # print('val:--- '  ,val, type(val))
            link_to_tag = val.get(atr)
            # print('link_to_tag:   ',link_to_tag)
            if check_local_link(url, link_to_tag):
                full_path_to_link = urljoin(url, link_to_tag)
                # print(full_path_to_link, ' !!!!!!!!!!!!!!@!@!!!!!!!')
                path_name = get_name(url, dir=True,
                                     full_link=full_path_to_link, directory=dir)
                print('path_name_tp_file;   ', path_name)
                link_bytes = requests.get(full_path_to_link,
                                          timeout=1, headers=header)
                val[atr] = path_name
                loader(os.path.join(dir, path_name), link_bytes.content)


def check_scripts_for_src():
    pass


def get_tags_to_change(data) -> list:
    # print('222222222222')
    # bs = get_bs(data)
    all_tags = []
    for tag, atrr in TAGS_FOR_DOWNLOAD.items():
        # print(TAGS_FOR_DOWNLOAD)
        # print(tag, val)
        all_tags.append((atrr, data.find_all(tag, {atrr: True})))
    print('222222222222', all_tags, len(all_tags))
    return all_tags


def loader(path_name, link_bytes):
    with open(f'{path_name}', 'wb') as f:
        f.write(link_bytes)
        print(f'Изображение {os.path.abspath(path_name)} успешно скачано!')
    time.sleep(randint(1, 2))


def get_response(url, path):
    # print(path)
    if not os.path.exists(path):
        raise IsADirectoryError('Directory not found bla bla')
    response = requests.get(url, timeout=1, headers=header)
    response.raise_for_status()
    return response


def saver(response, path, mode='w'):
    # print(response)
    with open(path, mode, encoding='utf-8') as file:
        file.write(response.prettify())


def get_bs(response):
    return BeautifulSoup(response, 'html.parser')


def create_dir(path):
    os.mkdir(path)


def check_local_link(url_1, url_2):
    home_url_parse = urlparse(url_1).netloc
    download_url_parse = urlparse(url_2).netloc
    # print(home_url_parse, link_to_download)
    if home_url_parse in download_url_parse or download_url_parse == '':
        # print('True')
        return True
    # print('False')
    return False


def get_urlparse(path: str):
    urlparse_result = urlparse(path.strip('/'))
    name, ext = os.path.splitext(urlparse_result.path)
    name = urlparse_result.netloc + name
    # print('it\'s is urlparser, name and exr: ', urlparse_result, name, ext)
    return urlparse_result, name, ext


def get_name(path, dir=None, file=None, full_link=None, directory=None):
    url_result, tail, ext = get_urlparse(path)
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
    if dir:
        try:
            # print('555556', res)
            create_dir(os.path.join(directory, res + '_files'))
            # print('5555', res)
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
