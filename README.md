# Send2Instapaper

mac OS Automator service for saving links to Instapaper

This simple project consists of two bits:

- mac OS Automator workflow which grabs link urls and calls the python script
- Python script send3instapaper.py which adds link to Instapaper account. You can use the script from commandline independently.
```
python send3instapaper.py -h
usage: send3instapaper.py [-h] [-n] [-u USER] source

Adds url to Instapaper

positional arguments:
  source                url of an article.

optional arguments:
  -h, --help            show this help message and exit
  -n, --notification    show notification via terminal-notifier (default:
                        False)
  -u USER, --user USER  user account at instapaper.com (default:
                        username@email.com)
```

## Installation:

- download and unzip
- move send3instapaper.py  [together with resources folder] to wherever you keep your scripts
- clik on 'Send 2 Instapaper.workflow' and add the workflow to Automator
- edit 'Run Shell Script' action in Automator and give it correct location of send3instapaper.py script
- add your Instapaper username (email) and password to keychain like this

```
security add-internet-password -a "user@email.com" -s instapaper.com -w This-is-secret-password

security find-internet-password -g -a user@email.com -s "instapaper.com"
```

- change default value of 'user' argument in send3instapaper.py getArgs() function to your account name
- OR you could also add USER argument in calling script in Automator

```
/usr/local/bin/python send3instapaper.py --user=user@email.com $@
```

Sounds complicated? No. This should be easy enough for you.

## Caveats:

- Send 2 Instapaper service should be now in Services menu now or sometimes under right click menu. This is however very tricky and depends on the context and the app you are using - there are many ways to skin a cat  and there are also many ways to grab something upon a cursor and extract a link in mac OS. 
I am using a simple one - grab a text in any application and extract URL action. It works in browser bar and on a web page and that's good enough for me. I had been experimenting with smarter ways of url extraction but either it gets more complicated then I am wishing spend my time on or it is unreliable. Or both. 
- There are alternative ways to run a script in Automator - for example you could choose '/usr/bin/python' as your shell and put script into Automator. Or you could make a script executable.
I am calling script this way cause I am using brew python and python is expecting some libraries and it works for me. 
- I like this script cause it uses request. You could find on github similiar scripts that use urllib. I am no fan of calling urllib.
- send3instapaper creates and keeps a log in a folder. You could look for errors - there. 
- I might add notifications for added links in a future.

## Benefits:

- Now you have your private service that resides on your computer and is universal between browsers. You could now remove browser add-ons that you have used for saving to Instapaper. 
- Nothing - expcept for sending a link - leaves your computer. 
- Ask yourself if you could really trust closed source add-on that requires access to you entire browsing activity? And which requries that you be logged to your Instapaper account all the time? 

## Credits:

I have started from defunct project [Send-To-Instapaper-OSX-Service
](https://github.com/Sankra/Send-To-Instapaper-OSX-Service) as an inspiration. 

