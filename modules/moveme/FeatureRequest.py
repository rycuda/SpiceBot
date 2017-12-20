#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import json
import requests
import ConfigParser
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## Creds
config = ConfigParser.ConfigParser()
config.read("/etc/spicecred.txt")
USERNAME = config.get("configuration","username")
PASSWORD = config.get("configuration","password")
    
# Repo
REPO_OWNER = 'deathbybandaid'
REPO_NAME = 'sopel-modules'

@sopel.module.commands('feature','issue')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    maincommand = trigger.group(1)
    instigator = trigger.nick
    inputtext = get_trigger_arg(triggerargsarray, 0)
    if maincommand == 'feature':
        labels=['Feature Request']
        title='Feature Request'
        action = " requested"
    else:
        labels=['Issue Report']
        title='Issue Report'
        action = " found an issue"
    if not inputtext:
        bot.say("What feature/issue do you want to post?")
    else:
        body = str(get_trigger_arg(triggerargsarray, 0))
        body = str(instigator + action + ": " + body)
        make_github_issue(bot, body, labels, title)

def make_github_issue(bot, body, labels, title):
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    issue = {'title': title,
             'body': body,
             'labels': labels}
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        bot.say("Successfully created " + title)
    else:
        bot.say("Could not create " + title)
        bot.say(str('Response:' + r.content))