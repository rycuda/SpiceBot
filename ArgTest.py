import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    channel = get_trigger_arg(bot.channels, 1)
    bot.say(str(channel))
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    simulatedvaluearray = ['5+','5-','5<','5>','last','5^7','5!']
    for i in range(0,totalarray):
        arg = get_trigger_arg(triggerargsarray, i)
        bot.say("arg " + str(i) + " = " + str(arg))
    for x in simulatedvaluearray:
        value = get_trigger_arg(triggerargsarray, x)
        if value != '':
            bot.say("arg " + str(x) + " = " + str(value))
        else:
            bot.say("arg " + str(x) + " is empty")
