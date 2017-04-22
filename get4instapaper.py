#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Grab HTML of article in Chrome [to avoid paywalls],
# save to file necessary parts, create markdown, send to Instapaper
# To create epub use: pandoc -s -c _html/ft.css  _html/*.html -o "FT
# $(date +"%d-%m-%Y").epub"

import sys
import os
import subprocess
import argparse
import logging
import re
import instapaper

API_key = "INSTAPAPER_API_KEY"


def slugify(str):
    slug = re.sub(r"[^\w]+", " ", str)
    slug = "-".join(slug.lower().strip().split())
    return slug


def get_keychain_pass(account=None, server=None):
    params = {
        'security': '/usr/bin/security',
        'command': 'find-internet-password',
        'account': account,
        'server': server
    }

    command = "%(security)s %(command)s -g -a %(account)s -s %(server)s -w" \
        % params
    logging.info(command)
    try:
        password = subprocess.getoutput(command)
        return password
    except Exception as e:
        logging.exception('Could not get password from keychain')
        raise


def get_instapaper(folder="unread", limit=10, text=True,
        instapaper_user='user@example.com') -> None:

    logging.info('instapaper_user = ' + instapaper_user)
    try:
        API_secret = get_keychain_pass(API_key, 'instapaper.com')
        I = instapaper.Instapaper(API_key, API_secret)
        instapaper_pass = get_keychain_pass(instapaper_user, 'instapaper.com')
        I.login(instapaper_user, instapaper_pass)

        marks = I.bookmarks(folder, limit)
        for m in marks:
            logging.info('Article: ' + m.title)
            print(m.title)
            if text:
                process_article(m.title, None, m.text)
            else:
                process_article(m.title, m.html, None)

    except Exception as e:
        logging.exception('Error retrieving Instapaper articles')
        raise


def get_folders(instapaper_user='user@example.com') -> None:

    logging.info('instapaper_user = ' + instapaper_user)
    try:
        API_secret = get_keychain_pass(API_key, 'instapaper.com')
        I = instapaper.Instapaper(API_key, API_secret)
        instapaper_pass = get_keychain_pass(instapaper_user, 'instapaper.com')
        I.login(instapaper_user, instapaper_pass)

        folders = I.folders()
        for f in folders:
            # print(f)
            # for k, v in f.items():
            #     print(k, v)
            print(f['folder_id'],  '\t', f['title'])

    except Exception as e:
        logging.exception('Error retrieving Instapaper folders')
        raise


def get_folder_id(folder_name, instapaper_user='user@example.com') -> None:

    logging.info('instapaper_user = ' + instapaper_user)
    try:
        API_secret = get_keychain_pass(API_key, 'instapaper.com')
        I = instapaper.Instapaper(API_key, API_secret)
        instapaper_pass = get_keychain_pass(instapaper_user, 'instapaper.com')
        I.login(instapaper_user, instapaper_pass)
        folders = I.folders()
        for f in folders:
            if folder_name in f['title']:
                print(f['title'])
                print(f['folder_id'])
                return f['folder_id']

    except Exception as e:
        logging.exception('Error retrieving Instapaper folders')
        raise


def process_article(article_title, article_html, article_text=None) -> None:
    html_filename = "resources/_tmp/" + slugify(article_title) + u".html"

    try:
        with open(html_filename, 'w+') as a:
            a.seek(0)
            a.write('<!DOCTYPE html>\n<html>\n<head>\n')
            a.write(
                '<meta http-equiv=“Content-Type” content=“text/html; charset=utf-8”>\n')
            a.write('<link rel="stylesheet" href="iBooks.css">\n')
            if article_title is not None:
                a.write('<title>' + article_title + '</title>\n')
            a.write('</head>\n<body>\n')
            if article_title is not None:
                # Don't use h1 for title (cause of pandoc/epub). Lame!
                a.write('<h2>' + article_title + '</h2>\n')
            if article_html is not None:
                a.write(str(article_html))
            if article_text is not None:
                a.write('\n<div>\n')
                for l in article_text.split('\n'):
                    if len(l.strip()) > 0:
                        a.write('<p>' + l + '</p>\n')
                a.write('\n</div>\n')
            a.write('\n</body>\n</html>\n')

        logging.info('Finished processing article')

    except Exception as e:
        logging.exception("Fatal error in __main__ loop")
        raise
    logging.info('Article: ' + article_title + ' parsed')


def getArgs(argv=None):
    parser = argparse.ArgumentParser(description='Download articles from \
                    Instapaper and create epub file',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--download', default=False,
                    action="store_true",
                    help='Do download articles')
    parser.add_argument('-l', '--list', default=False,
                    action="store_true",
                    help='List folders and ids')
    parser.add_argument('--html', default=False,
                    action="store_true",
                    help='Download as HTML not text (has links, pics and better formatting - way slower and uses more data). Text is just fine in simple case. ')
    parser.add_argument('-f', '--folder', default=None,
                    help='Downloads from particular folder')
    parser.add_argument('-a', '--articles', default=10,
                    help='Number of articles to download')
    parser.add_argument('-e', '--epub', default=False,
                    action="store_true",
                    help='Create epub')
    return parser.parse_args(argv)


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='get4instapaper.log', level=logging.DEBUG,
                        format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S',)
    logging.info('--- get4instapaper.py logging started ---.')

    args = getArgs()
    download = args.download
    list_folders = args.list
    download_text = not args.html
    folder = args.folder
    articles = args.articles
    epub = args.epub
    if list_folders:
        folder_id = get_folders()
    if folder is not None:
        folder_id = get_folder_id(folder)
    else:
        folder_id = "unread"
    if download:
        print('-- removing html files')
        for fname in os.listdir('resources/_tmp/'):
            if fname.endswith('.html'):
                print(fname)
                os.remove('resources/_tmp/' + fname)
        print('-- html files removed')
        get_instapaper(folder_id, articles, download_text)
    if epub:
        subprocess.call('resources/_tmp/ft.sh'.split())

    logging.info('--- get4instapaper logging finished ---.')
