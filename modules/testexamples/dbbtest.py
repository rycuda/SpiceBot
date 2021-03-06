#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

import textwrap
import collections
import json

import requests

from sopel.logger import get_logger
from sopel.module import commands, rule, example, priority


@sopel.module.commands('dbbtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    bot.say("This is deathbybandaid's test module")
    
    for rules in bot._callables.values():
        for func in rules.values():
            if hasattr(func, "commands"):
                testing = str("{}.{} = {}".format(func.__module__, func.__name__, func.commands))
                bot.say(str(testing))
    
    #cmdarray = []
    #for cmds in bot.commands:
    #    for cmd in cmds:
    #        if str(cmd).endswith("]"):
    #            for x in cmd:
    #                cmdarray.append(x)
    #cmdlist = get_trigger_arg(cmdarray, 'list')
    #bot.say(str(cmdlist))
    #bot.say('The data directory is ' + str(shareddir))
    
    #for x in bot._command_groups:
    #    bot.say(str(x))
    
    #for k, v in bot._command_groups.items():
    #    bot.say("{}: {}".format(k, v))
    
