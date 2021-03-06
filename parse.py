#!script
from optparse import OptionParser
import sys, os, os.path
import logging

from django.conf import settings

# Explicitly set DEBUG to False to avoid memory leak
settings.DEBUG = False

PARSER_USAGE = """Usage: %prog action
Available actions: person, commitee, vote, bill"""

def setup_logging(console_level):
    "Setup logging system"

    if not os.path.exists("log"): os.mkdir("log")

    root = logging.getLogger()
    formatter = logging.Formatter('%(name)s: %(message)s')

    handler = logging.FileHandler('log/parsing.error.log', 'w')
    handler.setLevel(level=logging.ERROR)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    handler = logging.FileHandler('log/parsing.log', 'w')
    handler.setLevel(level=logging.DEBUG)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    handler = logging.StreamHandler()
    handler.setLevel(getattr(logging, console_level.upper()))
    handler.setFormatter(formatter)
    root.addHandler(handler)

    root.setLevel(logging.DEBUG)


def parse_args():
    "Parse command line arguments"

    parser = OptionParser(usage=PARSER_USAGE)
    parser.add_option('-m', '--method', default='main',
                      help='Which parser method should be run')
    parser.add_option('-f', '--force', action="store_true",
                      help='Re-parse all data whether or not it has changed.')
    parser.add_option('-l', '--level', default='info',
                      help='Default logging level')
    parser.add_option('--disable-events', action='store_true', default=False,
                      help='Disable events processing')
    parser.add_option('--disable-indexing', action='store_true', default=False,
                      help='Disable synchronous indexing')
    parser.add_option('--congress',
                      help='Limit parsing to the specified congress')
    parser.add_option('--slow', action='store_true',
                      help='Slow down parsing so we don\'t interfere with other processes.')
    parser.add_option('--filter',
                      help='Only process files matching a regex.')
    kwargs, args = parser.parse_args()
    if not args:
        parser.print_usage()
        sys.exit()
    return kwargs, args


def main():
    kwargs, args = parse_args()

    setup_logging(kwargs.level)
    parser = __import__('parser.%s_parser' % args[0], globals(), locals(), ['xxx'])
    getattr(parser, kwargs.method)(kwargs)
    logging.debug('Done')

if __name__ == '__main__':
    main()

