import logging
import os
from page_loader.supports_files import change_response
from progress.bar import FillingSquaresBar

from page_loader.url import generate_path


def download(url: str, output_dir: str = None) -> str:
    logging.info(f'{37 * "*"} Start program {37 * "*"}')
    logging.debug(f'Logger was initialized for module {__name__}')

    if not os.path.exists(output_dir):
        logging.error(f'The specified directory'
                      f' does not exist or is a file {output_dir}')
        raise FileNotFoundError

    files_to_download, soup = change_response(url, output_dir)
    page_path = os.path.join(output_dir, generate_path(url) + '.html')
    loader(files_to_download)

    bar = FillingSquaresBar(f'Download page to {page_path}', max=1)
    bar.next()
    with open(page_path, 'w', encoding='utf-8') as file:
        file.write(soup)
        bar.finish()

    logging.debug(f'Save file in {page_path}')
    logging.info(f'{37 * "*"} End program {37 * "*"}')
    return page_path


def loader(files_to_load: str) -> str:
    for path_name, link_for_load in files_to_load.items():
        bar = FillingSquaresBar(f'Download file to {path_name}', max=1)
        logging.debug(f'save content in {path_name}')
        with open(path_name, 'wb') as f:
            f.write(link_for_load.content)
            bar.next()
        bar.finish()
        logging.debug(f'Файл {os.path.abspath(path_name)}'
                      f' успешно скачан!')
