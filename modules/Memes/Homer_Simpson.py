#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('homer')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    goodarray = ['good','g']
    badarray = ['bad','b','bad?','good?']
    goodorbad = get_trigger_arg(bot, triggerargsarray, 0) or 'bad'
    if goodorbad in goodarray:
        message = "WooHoo!"
    elif goodorbad in badarray:
        message = "D'ooooh!"
    else:
        message = str("mmmmmmm " + goodorbad + "!")
    bot.say(message)
