#!/urs/bin/env python3
import sys

from page_loader import download
from page_loader.cli import parse
from page_loader.exceptions import KnownError, AllErrors


def main():
    try:
        args = parse()
        download(args.url, args.path)
    except KnownError:
        sys.exit(1)
    except AllErrors:
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
