import sopel
from sopel.module import event, rule
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('chanreport')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    commandused = get_trigger_arg(triggerargsarray, 1)
    if not commandused:
        bot.say("What report do you want?")
    elif commandused == 'inactive':
        bot.say("WIP")
        # logic for if the user has been in the room for X time but hasn't said anything
        # and is still currently in the room
        # maybe also list how many times they joined and left the room during that time
        

# timestamp when they last spoke
#@thread(False)
#@rule('(.*)')
#@priority('low')
#def note(bot, trigger):
#    if not trigger.is_privmsg:
#        bot.db.set_nick_value(trigger.nick, 'seen_timestamp', time.time())
        
# join monitoring
#@event('JOIN')
#@rule('.*')
#def greeting(bot, trigger):
#    bot.say("hello " + trigger.nick)
