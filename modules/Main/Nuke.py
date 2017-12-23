#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('nuke','killit','terminate')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    ## Initial ARGS
    triggerargsarray = create_args_array(trigger.group(2)) ## triggerarg 0 = commandused
    commandused = trigger.group(1)
    target = get_trigger_arg(triggerargsarray, 1) or 'notarget'
    if commandused == 'nuke':
        nukeit(bot, trigger, triggerargsarray)
    elif commandused == 'killit':
        killitnow(bot, trigger, triggerargsarray)
    elif commandused == 'terminate':
        terminateit(bot, trigger, triggerargsarray, target)

def nukeit(bot, trigger, triggerargsarray):
    bot.say("Nuke it from orbit... it's the only way to be sure?")
    
def killitnow(bot, trigger, triggerargsarray):
    bot.say("Kill it with fire. Now.")

def terminateit(bot, trigger, triggerargsarray, target):
    if target == 'notarget':
        bot.say("Terminate it with extreme prejudice.")
    elif target:
        bot.action("terminates "+ target +" with extreme prejudice.")
