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


import np

@sopel.module.commands('chantest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    cmdarray = []
    for cmds in bot.command_groups.items():
        arrayconvert = np.array(cmds)
        for x in arrayconvert:
            bot.say(str(x))
        
        
        #cmdarray.append(cmd)
    #for x in cmdarray:
    #    dataset_array = []
    #    for j in x.split(','):
    #        bot.say(str(j))

    
    
    #for cmd in bot.command_groups.items():
    #    bot.say(str(cmd))
    
    
    #for cmds in collections.OrderedDict(sorted).items():
    #    for cmd in cmds:
    #        cmdarray.append(cmds)
    #cmdlist = get_trigger_arg(cmdarray, 'list')
    #bot.say(str(cmdarray))
    #
    #for u in bot.users:
    #    bot.say(u)
    
