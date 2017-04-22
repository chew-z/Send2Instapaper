#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Grab HTML of article in Chrome [to avoid paywalls], save to file only necessary parts, create markdown, send to Instapaper
# To create epub use: pandoc -s -c _html/ft.css  _html/*.html -o "FT
# $(date +"%d-%m-%Y").epub"

import sys
import requests
import re
import html2text
import datetime
from bs4 import BeautifulSoup
import argparse
import logging
import instapaper
import subprocess


API_key = "INSTAPAPER_API_KEY"

def get_keychain_pass(account=None, server=None):
    params = {
        'security': '/usr/bin/security',
        'command': 'find-internet-password',
        'account': account,
        'server': server
    }

    command = "%(security)s %(command)s -g -a %(account)s -s %(server)s -w" % params
    logging.info(command)
    try:
        password = subprocess.getoutput(command)
        return password
    except Exception as e:
        logging.exception('Could not get password from keychain')
        raise


def send_instapaper(url=None, content=None, title=None, description=None, instapaper_user='user@example.com') -> None:
    params = {
        'url': url,
        'content': content,
        'title': title,
        'description': description
    }
    try:
        API_secret = get_keychain_pass(API_key, 'instapaper.com')
        I = instapaper.Instapaper(API_key, API_secret)
        instapaper_pass = get_keychain_pass(instapaper_user, 'instapaper.com')
        I.login(instapaper_user, instapaper_pass)
        b = instapaper.Bookmark(I, params)
        b.save()
        logging.info('Article: ' + title + ' saved to Instapaper')
    except Exception as e:
        logging.exception('Error sending article to Instapaper')
        raise


def process_article(article_title, article_filename='resources/article.htm') -> None:
    html_filename = "resources/_html/" + article_title + u".html"
    md_filename = "resources/_md/" + article_title + u".md"
    h = html2text.HTML2Text()
    # h.decode_errors = 'replace'
    h.unicode_snob = True
    h.ignore_links = True
    h.skip_internal_links = True
    h.ignore_anchors = True
    h.ignore_images = False
    h.body_width = 0
    # h.unifiable = True
    # h.escape_snob = True
    # h.re_unescape = True
    try:
        # read from article.htm (Automator service saves html form Chrome into
        # this file)
        with open(article_filename, 'r') as r:
            html = r.read()
        soup = BeautifulSoup(html, "html.parser")
        # style = soup.find("style", class_="n-layout-head-css")
        if (title is not None):
            header = title
        else:
            header = soup.find("h1", class_="topper__headline").get_text("\t", strip=True)
        logging.info('header: ' + header)
        lead = soup.find("div", class_="topper__standfirst")
        logging.info('lead.text: ' + lead.text)
        article = soup.find(
            "div", class_= re.compile("article__body n-content-body.*"))
        if article.str is not None:
            logging.info('Scraped some article content')
        with open(html_filename, 'w') as a:
            a.write('<!DOCTYPE html>\n<html>\n<head>\n')
            a.write(
                '<meta http-equiv=“Content-Type” content=“text/html; charset=utf-8”>\n')
            a.write('<link rel="stylesheet" href="ft.css">\n')
            a.write('<title>' + header + '</title>\n')
            # if style is not None:
            # a.write(str('<style class="n-layout-head-css">' + style.text + '</style>\n'))
            a.write('</head>\n<body>\n')
            if header is not None:
                # Don't use h1 for title (cause of pandoc/epub). Lame!
                h.feed('<h1>' + header + '</h1>')
                a.write('<h1 class="article-headline">' +
                        header + '</h1>\n')

            if lead is not None:
                h.feed('<h2>' + lead.text + '</h2>')
                a.write('<h2 class="article__header-secondary">' +
                        lead.get_text(" | ", strip=True) + '</h2>\n')

            if article is not None:
                a.write(str(article))
                h.feed(str(article))
            a.write('\n</body>\n</html>\n')
            # processing in chunks - breaks paragraph flow in places of links
            # for chunk in article.stripped_strings:
            #     h.feed('<p>'+ chunk +'</p>')
        text = h.close()
        yaml = "---\n"
        yaml += "title: " + header + "\n"
        yaml += "publisher:  Financial Times\n"
        yaml += "lang: en-GB\n"
        # yaml += "stylesheet: _css/iBooks.css\n"
        yaml += "creator: ft2text.py\n"
        yaml += "date: " + today.strftime('%Y-%m-%d') + "\n"
        yaml += "---\n\n"
        if text is not None:
            with open(md_filename, "w") as w:
                w.write(yaml)
                w.write(text)
    except Exception as e:
        logging.exception("Fatal error in __main__ loop")
        raise
    logging.info('Article: ' + article_title + ' parsed')


def getArgs(argv=None):
    parser = argparse.ArgumentParser(description='Saves ft.com articles [from Chrome via service] as markdown and html preview',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--title', default=None,
                        help='Article title [used for filename]')
    parser.add_argument('-u', '--url',
                        help='url of an article. [used for Instapaper url]')
    parser.add_argument('-i', '--instapaper', default=False,
                        action="store_true",
                        help='Save also article to Instapaper]')
    return parser.parse_args(argv)


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='ft2text.log', level=logging.DEBUG,
                        format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S',)
    logging.info('--- ft2text.py logging started ---.')

    today = datetime.date.today()
    args = getArgs()
    title = args.title
    url = args.url
    logging.info(title)
    logging.info(url)
    process_article(title)
    if args.instapaper:
        # we are sending article grabed from Chrome to avoid paywall login
        # also article is purified from css, javascript etc.
        with open('resources/article.htm', 'r') as article:
            content = article.read()
        # strip first and last ie quotes from url quoted form
        url = args.url[1:-1]
        send_instapaper(url, content, title)
    logging.info('--- ft2text.py logging finished ---.')
