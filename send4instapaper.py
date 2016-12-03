#coding: utf-8
# This version send4instapaper.py is for use on iOS ( with Pythonista)
import requests
import sys
import re
# Pythonista specific
import clipboard
import appex
import keychain

class Instapaper(object):
  def __init__(self, username, password):
    self.username = str(username)
    self.password = str(password)
    self.auth_url = 'https://www.instapaper.com/api/authenticate'
    self.add_url  = 'https://www.instapaper.com/api/add'

  def check_login(self):
    print('check_login')
    r = requests.get(self.auth_url, auth=(self.username, self.password))
    if r.status_code == 200:
      return True
    elif r.status_code == 403:
      err = '403: wrong username/password'
    else:
      err = '500: internal error'
    print(err)
    raise ValueError('Could not log into Instapaper', err)
    return False

  def add(self, url):
    print('add_url')
    url = self.add_url + '?url=' + url
    r = requests.get(url, auth=(self.username, self.password))
    if r.status_code == 201:
      t = r.headers['X-Instapaper-Title'];
      print("[%s] added!" % t)
      return t
    elif r.status_code == 400:
      err = '400: bad reques, url needed'
    elif r.status_code == 403:
      err = '403: wrong username/password'
    else:
      err = '500: internal error'
    print(err)
    raise ValueError('Could not add article to Instapaper', err)
    return None

if __name__ == '__main__':
  if not appex.is_running_extension():
    url = clipboard.get()
  else:
    url = appex.get_url()
    # hint - appex uses separate keychain
  print(url)
  instapaper_user = 'user@email.com'
  instapaper_pass = keychain.get_password('Instapaper', instapaper_user)
  try:
    instapaper = Instapaper(instapaper_user, instapaper_pass)
    title = instapaper.add(url)
    m = 'Article: ' +  title + ' saved to Instapaper.'
    print(m)
  except Exception as e:
    print("Error in __main__ loop")

