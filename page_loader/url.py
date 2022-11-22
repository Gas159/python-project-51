import os
import re
from urllib.parse import urlparse, urljoin


def generate_path(url):
    urlparse_result = urlparse(url)
    costume_name = urlparse_result.netloc + urlparse_result.path
    body, ext = os.path.splitext(costume_name)
    name_of_path = generate_name(body)
    return name_of_path + ext


def generate_dir(url: str, directory_name: str, link_to_tag: str):
    short_dir_name = generate_path(url) + '_files'
    dir_path = os.path.join(directory_name, short_dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    shor_file_name = generate_path(urljoin(url, link_to_tag))
    body, ext = os.path.splitext(shor_file_name)
    if not ext:
        ext = '.html'
    file_name_to_change = os.path.join(short_dir_name, (body + ext))
    return file_name_to_change, os.path.join(dir_path, (body + ext))


def generate_name(path: str) -> str:
    return re.sub(r'\W', '-', path.strip('/'))
