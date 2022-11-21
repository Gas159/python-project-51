from urllib.parse import urlparse


def check_local_link(url_1, url_2):
    home_url_parse = urlparse(url_1).netloc
    download_url_parse = urlparse(url_2).netloc
    if home_url_parse == download_url_parse or download_url_parse == '':
        return True
    return False
