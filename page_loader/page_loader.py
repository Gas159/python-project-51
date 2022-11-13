import logging
import os

from page_loader.exceptions import KnownError
from page_loader.supports_files \
    import get_response, change_response, get_bs, \
    generate_path, check_valid_path_and_url
from progress.bar import FillingSquaresBar



def download(url: str, cli_path=None) -> str:
    logging.info(f'{37 * "*"} Start program {37 * "*"}')
    logging.debug(f'Logger was initialized for module {__name__}')

    if not os.path.exists(cli_path):
        logging.error(f'The specified directory'
                      f' does not exist or is a file {cli_path}')
        raise KnownError

    response = get_response(url)
    page_path = os.path.join(cli_path, generate_path(url))
    soup = get_bs(response.text)
    change_response(url, soup, cli_path)
    saver(soup, page_path)
    logging.info(f'{37 * "*"} End program {37 * "*"}')
    return page_path


def saver(response, path, mode='w'):
    bar = FillingSquaresBar(f'Download page to {path}', max=1)
    bar.next()
    with open(path, mode, encoding='utf-8') as file:
        file.write(response.prettify())
        bar.finish()
    logging.debug(f'Save file in {path}')
