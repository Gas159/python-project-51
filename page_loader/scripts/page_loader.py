#!/urs/bin/env python3
import os

import requests
import logging
import sys

from page_loader import download

# from page_loader.cli import parse
# from page_loader.my_dir.click1 import parse_with_click

FORMAT = "%(name)s %(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def main():
    try:
        # args = parse()
        # print(download(args.url, args.path))

        import click

        @click.command()
        @click.option('-o', default=os.getcwd(), help='Number of greetings.')
        @click.option('--path')
        # prompt='You url: ',              help='The person to greet.')
        def parse_with_click(o, path):
            # """Simple program that greets NAME for a total of COUNT times."""
            # for x in range(count):
            #     click.echo(f"Hello {name}!")
            print(download(path, o))
            click.echo('End programm')

        parse_with_click()

    except requests.exceptions.HTTPError:

        logging.error('This page was not found')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        logging.error('Connection error')
        sys.exit(1)
    except requests.exceptions.RequestException:
        logging.error('Other connection error')
        sys.exit(1)
    except FileNotFoundError:
        logging.error('The specified directory does not exist or is a file')
        sys.exit(1)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
