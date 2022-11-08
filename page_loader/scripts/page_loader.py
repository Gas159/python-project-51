#!/urs/bin/env python3
import logging
import sys

from page_loader import download
from page_loader.cli import parse
from page_loader.exceptions import KnownError, AllErrors

# FORMAT = '%(message)s'
# logging.basicConfig(level=logging.DEBUG)
FORMAT = "%(name)s %(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def main():

    try:
        args = parse()
        download(args.url, args.path)
        # sys.exit(0)
    except KnownError:
        sys.exit(1)
    except AllErrors:
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    # else:
    #     sys.exit(0)


if __name__ == '__main__':
    main()
