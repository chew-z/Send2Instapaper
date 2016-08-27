#!/usr/bin/env python
# script used by mac OS Automator Service to add links to Instapaper
# works also with python3 but in OSX you have to install requests

import argparse
import requests
import sys
import re
import commands
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
            logging.error('403: wrong username/password')
        else:
            logging.error('500: internal error')
        return False

    def add(self, url):
        url = self.add_url + '?url=' + url
        r = requests.get(url, auth=(self.username, self.password))
        if r.status_code == 201:
            title = r.headers['X-Instapaper-Title'];
            logging.info("[%s] added!" % title)
            return True
        elif r.status_code == 400:
            logging.error('400: bad reques, url needed')
        elif r.status_code == 403:
            logging.error('403: wrong username/password')
        else:
            logging.error('500: internal error')
        return False

def get_keychain_pass(account=None, server='instapaper.com'):
    params = {
        'security': '/usr/bin/security',
        'command':  'find-internet-password',
        'account':  account,
        'server':   server
    }

    command = "%(security)s %(command)s -g -a %(account)s -s %(server)s" % params
    outtext = commands.getoutput(command)
    return re.match(r'password: "(.*)"', outtext).group(1)

def getArgs(argv=None):
    # Command line arguments.
    parser = argparse.ArgumentParser(description = 'Add url to Instapaper',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('source', help='url of an article.')
    parser.add_argument('-u', '--user',
                        default="username@email.com",
                        help='user account at instapaper.com')
    return parser.parse_args(argv)

if __name__ == '__main__':
    args = getArgs()
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='instapaper.log', level=logging.DEBUG,
                        format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S',)
    logging.info('--- send3toinstapaper logging started ---.')
    url = args.source
    logging.info(url)
    instapaper_user = args.user
    try:
        instapaper_pass = get_keychain_pass(instapaper_user, 'instapaper.com')
        instapaper = Instapaper(instapaper_user, instapaper_pass)
        instapaper.add(url)
    except Exception as e:
        logging.exception("Fatal error in __main__ loop")
