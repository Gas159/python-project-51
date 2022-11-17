#!/urs/bin/env python3
import requests
import logging
import sys

from page_loader import download
from page_loader.cli import parse
from page_loader.exceptions import KnownError

FORMAT = "%(name)s %(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def main():
    try:
        args = parse()
        print(download(args.url, args.path))
    # except requests.exceptions.RequestException as e:
    #     logging.error(f'Some went wrong .\n\n{e}')
    #     print('1')
    #     # raise AllErrors() from e
    #     sys.exit(1)
    # except KnownError:
    #     passrequests.exceptions.RequestException
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        sys.exit(1)

    # except requests.exceptions.HTTPError:
    #     print('2')
    #     sys.exit(1)
    # except requests.exceptions.ConnectionError:
    #     print('12121')
    #     sys.exit(1)
    # except requests.exceptions:
    #     print('4')
    #     sys.exit(1)

    except KnownError:
        sys.exit(1)
    # except AllErrors:
    #     sys.exit(1)
    # except KeyboardInterrupt:
    #     sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
