import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('drugs')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        bot.say(trigger.nick + " contemplates selling everything and moving somewhere tropical to sell drugs on a beach.")
