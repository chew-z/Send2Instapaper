#!/usr/bin/env python
# script used by mac OS Automator Service to add links to Instapaper
# python3  doesn't have commands

import argparse
import requests
import sys
import re
# commands is python2 only!
# import commands
import subprocess
import logging

class Instapaper(object):
    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)
        self.auth_url = 'https://www.instapaper.com/api/authenticate'
        self.add_url  = 'https://www.instapaper.com/api/add'

    def check_login(self):
        r = requests.get(self.auth_url, auth=(self.username, self.password))
        if r.status_code == 200:
            return True
        elif r.status_code == 403:
            err = '403: wrong username/password'
        else:
            err = '500: internal error'
        logging.error(err)
        raise ValueError('Could not log into Instapaper', err)
        return False

    def add(self, url):
        url = self.add_url + '?url=' + url
        r = requests.get(url, auth=(self.username, self.password))
        if r.status_code == 201:
            t = r.headers['X-Instapaper-Title'];
            logging.info("[%s] added!" % t)
            return t
        elif r.status_code == 400:
            err = '400: bad reques, url needed'
        elif r.status_code == 403:
            err = '403: wrong username/password'
        else:
            err = '500: internal error'
        logging.error(err)
        raise ValueError('Could not add article to Instapaper', err)
        return None

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
        # password = commands.getoutput(command)
        password = subprocess.getoutput(command)
        return password
        # outtext = commands.getoutput(command)
        # return re.match(r'password: "(.*)"', outtext).group(1)
    except Exception as e:
        logging.exception('Could not get password from keychain')
        raise

def send_notification(message=None):
    params = {
        'notifier': '/usr/local/bin/terminal-notifier',
        'message':  message,
        'title':  'send3instapaper.py',
        'url':   'https://www.instapaper.com/u',
        'icon':  './resources/Instapaper.icns',
        'image':  '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ClippingText.icns'
    }

    command = "%(notifier)s -message \"%(message)s\" -title \"%(title)s\" -open \"%(url)s\" -appIcon \"%(icon)s\" -contentImage \"%(image)s\"" % params
    logging.info(command)
    try:
        # return commands.getoutput(command)
        return subprocess.getoutput(command)
    except Exception as e:
        logging.exception('Sending notification failed')
        raise

def getArgs(argv=None):
    # Command line arguments.
    parser = argparse.ArgumentParser(description = 'Add url to Instapaper',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('source', help='url of an article.')
    parser.add_argument('-n', '--notification', default=False,
                        action="store_true",
                        help='show notification via terminal-notofier')
    parser.add_argument('-u', '--user', default="username@email.com",
                        help='user account at instapaper.com')
    return parser.parse_args(argv)

if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='instapaper.log', level=logging.DEBUG,
                        format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S',)
    logging.info('--- send3toinstapaper logging started ---.')

    args = getArgs()
    url = args.source
    notify = args.notification
    instapaper_user = args.user
    logging.info(url)

    try:
        instapaper_pass = get_keychain_pass(instapaper_user, 'instapaper.com')
        instapaper = Instapaper(instapaper_user, instapaper_pass)
        title = instapaper.add(url)
        if notify and title is not None:
            m = 'Article: ' +  title + ' saved to Instapaper.'
            send_notification(m)
    except Exception as e:
        logging.exception("Fatal error in __main__ loop")
