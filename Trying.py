#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('trying')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(triggerargsarray, 1)
    if target:
        phrase = target.strip()
        if phrase.startswith('to'):
            parta = phrase
            partb = phrase.replace('to','').strip()
        else:
            parta = str("to " + phrase)
            partb = phrase
        statement = str("Are you trying " + parta + "? 'Cuz that's how you " + partb + "!!!")
        bot.say(statement)
