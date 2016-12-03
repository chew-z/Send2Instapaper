#!/usr/bin/env python
# coding: utf-8
# script used by mac OS Automator Service to scrap webpage in markdown

import argparse
import requests
import sys
import re
import html2text
import json
import logging
import subprocess

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def read_from_clipboard():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def getArgs(argv=None):
    # Command line arguments.
    parser = argparse.ArgumentParser(description = 'Scrap url to Markdown',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('source', help='url of a webpage.')
    return parser.parse_args(argv)

if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='html3markdown.log', level=logging.DEBUG,
                        format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S',)
    logging.info('--- HTML 2 Markdown logging started ---.')

    args = getArgs()
    url = args.source
    logging.info(url)

    h = html2text.HTML2Text()
    html2text.decode_errors = 'replace'
    h.ignore_links = True
    h.skip_internal_links = True
    h.ignore_anchors = True
    h.ignore_images = True

    h.body_width = 0
    html2text.unifiable = True
    html2text.unicode_snob = True
    # html2text.escape_snob = True
    # html2text.re_unescape = True

    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            html_encoding = response.encoding
            logging.info(html_encoding)
            if html_encoding == 'ISO-8859-1':
                # request is falling back to ISO-8859-1 when you have a text/* response
                # and no content type has been specified in the response headers
                # https://github.com/kennethreitz/requests/issues/2086
                # TODO
                # better solution  is to look for <meta charset="utf-8"> <meta http-equiv="Content-Type">
                # http://stackoverflow.com/questions/36453359/
                logging.info('document is probably encoded with UTF-8 but requests identified it as ISO-8859-1')
                response.encoding = 'UTF-8'
                # html = html_raw.replace(u'Â', u'&nbsp;')
            html = response.text
        else:
            logging.error('-- HTTP respone not OK, exiting gracefully --')
            sys.exit(0)
        # print html
        text = h.handle(html)
        # print text
        write_to_clipboard(text)
    except Exception as e:
        logging.exception("Fatal error in __main__ loop")

    logging.info('--- HTML 2 Markdown logging finished ---.')
