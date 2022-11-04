import logging
import os
# import sys

from page_loader.requests_and_response \
    import get_response, change_response, get_bs, \
    generate_path, check_valid_path_and_url
from progress.bar import FillingSquaresBar

# FORMAT = '%(message)s'
# logging.basicConfig(level=logging.DEBUG, format=FORMAT)
# stream=sys.stderr
loger = logging.getLogger(__name__)


# fh = logging.FileHandler(f"{__name__}.log", mode='w')
# fh.setFormatter(logging.Formatter(
#     "%(name)s %(asctime)s %(levelname)s %(message)s"))
# fh.setLevel(logging.ERROR)
#
# loger.addHandler(fh)


def download(url: str, cli_path=None) -> str:
    loger.info(f'{37 * "*"} Start program {37 * "*"}')
    loger.debug(f'Logger was initialized for module {__name__}')

    check_valid_path_and_url(cli_path)
    response = get_response(url)
    page_path = os.path.join(cli_path, generate_path(url))
    soup = get_bs(response.text)
    change_response(url, soup, cli_path)

    saver(soup, page_path)
    loger.info(f'{37 * "*"} End program {37 * "*"}')
    return page_path


def saver(response, path, mode='w'):
    bar = FillingSquaresBar(f'Download page to {path}', max=1)
    bar.next()
    with open(path, mode, encoding='utf-8') as file:
        file.write(response.prettify())
        bar.finish()
    loger.debug(f'Save file in {path}')
