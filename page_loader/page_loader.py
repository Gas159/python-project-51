import logging
import os
from page_loader.exceptions import KnownError
from page_loader.requests_and_response \
    import get_response, change_response, get_bs, get_name
from progress.bar import FillingSquaresBar

FORMAT = '%(asctime)s :: %(name)s :%(lineno)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
loger = logging.getLogger(__name__)
loger.debug(f'Logger was initialized for module {__name__}')


def download(url: str, cli_path=os.getcwd()) -> str:
    check_valid_path(cli_path)
    loger.info('Start programm')

    response = get_response(url)
    page_path = os.path.abspath(os.path.join(cli_path, get_name(url,
                                                                file=True)))
    soup = get_bs(response.text)
    change_response(url, soup, cli_path)
    saver(soup, page_path)
    loger.debug(f'Page download sucсessfully in: {page_path}')
    loger.info('Close programm')
    return page_path


def saver(response, path, mode='w'):
    bar = FillingSquaresBar(f'Download page to {path}', max=1)
    bar.next()
    loger.debug(f'Save file in {path} with {mode}')
    with open(path, mode, encoding='utf-8') as file:
        file.write(response.prettify())
        bar.finish()


def check_valid_path(path_to_save_html):
    if not os.path.exists(path_to_save_html):
        loger.error(f'DirNotFound {path_to_save_html}')
        raise KnownError
