import sopel.module
from sopel import module, tools
import sys
import os
import random
#import Spicebucks.py
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *


#A roulette game to be used with Spicebucks.


@sopel.module.commands('roulette', 'spin')
def mainfunction(bot, trigger):
  enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, triggerargsarray):
  #get triggerwords from player to allow number,color and even/odd choices
  bot.say(trigger + ' spins the wheel')
  result = spinwheel
  #proccess array to determine if number is odd or even and color
  bot.say('The wheel stops on ' + result) 
  #payout based on results

def spinwheel
  random.seed()
  thenumber = random.randint(0,36)
  thecolor=random.randint(0,1)
  #return array with color and number
  return thenumber