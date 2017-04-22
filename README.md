# Send2Instapaper

Collection of my Instapaper related scripts.

This simple project consists of few bits:

- Python script send3instapaper.py which adds link to Instapaper account. You can use the script from commandline independently
- a variant of send3instapaper.py (called send4instapaper.py) that I use on iOS in Pythonista for saving links without bloating my iPhone with Instapaper app
- Python script sending to instapaper articles on ft.com (together with article HTML). It avoids paywall issue where the article content cannot be downloaded by instapaper.com through paywall
- Python script sending to instapaper articles (together with article HTML) in Chrome, Chromium. It avoids paywall issue
- Python script for downloading articles from instapaper.com and creating epub file using pandoc.
- Shell script ft.sh used to generate epub files form collection of html files.
- mac OS Automator workflow which grabs link url and calls the python script
- Another Automator workflow for saving web pages to Clipboard as markdown files (it is using html3md.py python script)



Most Python scripts have --help option with some explanation of options and parameters.


## Benefits:

- Now you have your private service that resides on your computer and is universal between browsers. You could now remove browser add-ons that you have used for saving to Instapaper. 
- Nothing - expcept for sending a link - leaves your computer. 
- Ask yourself if you could really trust closed source add-on that requires access to you entire browsing activity? And which requries that you be logged to your Instapaper account all the time? 

## Credits:

I have started from defunct project [Send-To-Instapaper-OSX-Service
](https://github.com/Sankra/Send-To-Instapaper-OSX-Service) as an inspiration. 

