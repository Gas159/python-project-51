import os
from urllib.parse import urljoin
import fake_useragent
import requests
import logging
from page_loader.url import generate_path, generate_dir
from page_loader.relevant_url import check_local_link
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

TAGS_FOR_DOWNLOAD = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def change_response(url, directory_name):
    logging.debug('Change response')
    response = get_response(url)
    tags = []
    data = BeautifulSoup(response.text, 'html.parser')
    page_path = os.path.join(directory_name, generate_path(url) + '.html')
    for tag, atr in TAGS_FOR_DOWNLOAD.items():
        tags.append((atr, data.find_all(tag, {atr: True})))

    all_links = {}

    for tag in tags:
        atr, values = tag

        for val in values:
            link_to_tag = val.get(atr)

            if check_local_link(url, link_to_tag):
                download_link = urljoin(url, link_to_tag)

                path_changed, path_name = generate_dir(
                    url, directory_name, link_to_tag)

                link_for_load = get_response(download_link)
                val[atr] = path_changed
                all_links[path_name] = link_for_load
    return all_links, page_path, data


def get_response(url):
    logging.debug(f'get response with requests.get({url})')
    response = requests.get(url, timeout=1, headers=header)
    response.raise_for_status()
    # soup = BeautifulSoup(response.text, 'html.parser')
    return response
