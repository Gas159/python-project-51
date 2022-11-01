import logging
import os
from page_loader.exceptions import KnownError
from page_loader.requests_and_response \
    import get_response, change_response, get_bs, get_name
from progress.bar import FillingSquaresBar

FORMAT = '%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
loger = logging.getLogger(__name__)

# loger_er = logging.getLogger(__name__)
fh = logging.FileHandler(f"{__name__}.log", mode='w')
fh.setFormatter(logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s"))
fh.setLevel(logging.ERROR)

loger.addHandler(fh)


def download(url: str, cli_path=os.getcwd()) -> str:
    loger.info(f'{30 * "*"} Start program! {30 * "*"}')
    loger.debug(f'Logger was initialized for module {__name__}')
    check_valid_path_and_url(url, cli_path)

    response = get_response(url)
    page_path = os.path.abspath(os.path.join(cli_path, get_name(url,
                                                                file=True)))
    soup = get_bs(response.text)
    change_response(url, soup, cli_path)
    saver(soup, page_path)
    loger.info(f'{30 * "*"} End program {30 * "*"}')
    return page_path


def saver(response, path, mode='w'):
    bar = FillingSquaresBar(f'Download page to {path}', max=1)
    bar.next()
    with open(path, mode, encoding='utf-8') as file:
        file.write(response.prettify())
        bar.finish()
    loger.debug(f'Save file in {path} with mode "{mode}"')


def check_valid_path_and_url(url, path_to_save_html):
    if not os.path.exists(path_to_save_html):
        loger.error(f'DirNotFound {path_to_save_html}')
        raise KnownError
