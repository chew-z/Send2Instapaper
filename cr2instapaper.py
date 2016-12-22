#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Grab HTML of article in Chrome, send to Instapaper as content aboiding trouble with paywalls
import argparse
import logging
import instapaper
import subprocess


def get_keychain_pass(account=None, server=None):
    params = {
        'security': '/usr/bin/security',
        'command':  'find-internet-password',
        'account':  account,
        'server':   server
    }

    command = "%(security)s %(command)s -g -a %(account)s -s %(server)s -w" % params
    logging.info(command)
    try :
        password = subprocess.getoutput(command)
        return password
    except Exception as e:
        logging.exception('Could not get password from keychain')
        raise

def send_notification(message=None):
    params = {
        'notifier': '/usr/local/bin/terminal-notifier',
        'message':  message,
        'title':  'cr2instapaper.py',
        'url':   'https://www.instapaper.com/u',
        'icon':  './resources/Instapaper.icns',
        'image':  '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ClippingText.icns'
    }

    command = "%(notifier)s -message \"%(message)s\" -title \"%(title)s\" -open \"%(url)s\" -appIcon \"%(icon)s\" -contentImage \"%(image)s\"" % params
    logging.info(command)
    try:
        return subprocess.getoutput(command)
    except Exception as e:
        logging.exception('Sending notification failed')
        raise

def getArgs(argv=None):
    # Command line arguments.
    parser = argparse.ArgumentParser(description =
                        'Saves articles [in Chrome via Automator service] passing content grabed from browser (also when logged in and behind paywall) rather then via Instapaper.',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--user', default="username@email.com",
                        help='user account at instapaper.com')
    parser.add_argument('-t', '--title', default=None,
                        help='Article title')
    parser.add_argument('-u', '--url',
                        help='Article url')
    parser.add_argument('-c', '--content',
                        help='Content as html/body/..')
    parser.add_argument('-f', '--file',
                        help='Content in file..')
    return parser.parse_args(argv)

if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='cr2instapaper.log', level=logging.DEBUG,
                        format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S',)
    logging.info('--- cr2instapaper.py logging started ---.')

    args = getArgs()
    instapaper_user = args.user
    title = args.title
    content = args.content
    url = args.url[1:-1]    # strip first and last ie quotes from url quoted form
    logging.info(url)
    logging.info(title)
    try:
        API_key = "e25b1a3dc611401988da0352d4955a7e"
        API_secret = get_keychain_pass(API_key, 'instapaper.com')
        I = instapaper.Instapaper(API_key, API_secret)
        instapaper_pass = get_keychain_pass(instapaper_user, 'instapaper.com')
        I.login(instapaper_user, instapaper_pass)

        if content is None:
            filename = args.file
            with open(filename, 'r') as article:
                content = article.read()
        if content is None:
            logging.info("Processing with empty content. Which is not the point. But..")
            content = ''

        b = instapaper.Bookmark(I, {'title': title, 'url': url, 'content': content})
        b.save()
        m = 'Article: ' +  title + ' saved to Instapaper.'
        send_notification(m)

    except Exception as e:
        logging.exception("Fatal error in __main__ loop")

    logging.info('--- cr2instapaper.py logging finished ---.')
