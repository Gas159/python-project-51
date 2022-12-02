from urllib.parse import urljoin
import requests
import logging
from page_loader.url import generate_dir, check_local_link
from bs4 import BeautifulSoup

TAGS_FOR_DOWNLOAD = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def prepare_response(url, directory_name):
    logging.debug('Change response')
    response = get_response(url)
    tags = []
    soup_content = BeautifulSoup(response.text, 'html.parser')
    for tag, attr in TAGS_FOR_DOWNLOAD.items():
        tags.append((attr, soup_content.find_all(tag, {attr: True})))

    all_links = {}

    for tag in tags:
        attr, values = tag

        for val in values:
            link_to_tag = val.get(attr)

            if check_local_link(url, link_to_tag):
                download_link = urljoin(url, link_to_tag)

                path_changed, path_name = generate_dir(
                    url, directory_name, link_to_tag)

                val[attr] = path_changed
                all_links[path_name] = download_link
    return all_links, soup_content.prettify()


def get_response(url):
    logging.debug(f'get response with requests.get({url})')
    response = requests.get(url, timeout=1)
    response.raise_for_status()
    return response
