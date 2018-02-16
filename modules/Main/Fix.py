#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

commandarray = ["add","remove","count","last"]
#add reset and sort list

@sopel.module.commands('fix')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    inchannel = trigger.sender
    databasekey = 'fixes'
    command = get_trigger_arg(triggerargsarray, 1)
    inputstring = get_trigger_arg(triggerargsarray, '2+')
    existingarray = get_botdatabase_value(bot, bot.nick, databasekey) or []
    if command in commandarray:
        if command == "add":
            if inputstring not in existingarray:
                adjust_botdatabase_array(bot, bot.nick, inputstring, databasekey, 'add')
                message = "Added to database."
            else:
                message = "That response is already in the database."
        elif command == "remove":
            if inputstring not in existingarray:
                message = "That response was not found in the database."
            else:
                adjust_botdatabase_array(bot, bot.nick, inputstring, databasekey, 'del')
                message = "Removed from database."
        elif command == "count":
            messagecount = len(existingarray)
            message = "There are currently " + str(messagecount) + " responses for that in the database."
        #elif command == "list":
        #    if inchannel.startswith("#"):
        #        message = "List can only be run in privmsg to avoid flooding."
        #    else:
        #        message = get_trigger_arg(existingarray, "list")
        elif command == "last":
            message = get_trigger_arg(existingarray, "last")
    else:
        message = get_trigger_arg(existingarray, "random") or ''
        if message == '':
            message = "No response found. Have any been added?"
    bot.say(message)
