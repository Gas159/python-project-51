#!/urs/bin/env python3
import requests
import logging
import sys

from page_loader import download
from page_loader.cli import parse

FORMAT = "%(name)s %(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def main():
    try:
        args = parse()
        print(download(args.url, args.path))

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
