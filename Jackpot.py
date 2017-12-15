import sopel.module
from sopel import module, tools
import sys
import os
import random
import Spicebucks
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('slots')
def mainfunction(bot, trigger):
  enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
  #using computer terms instead of fruit
  wheel = ['CPU', 'Modem', 'RAM', 'BSOD', 'Power Cord']
  wheel1 = pull(wheel)
  wheel2 = pull(wheel)
  wheel3 = pull(wheel)
 bot.say(wheel1 + wheel2 + wheel3)  
  

def deal(wheel):
  selected=random.ranint(0,len(wheel))
  reel=wheel[selected]
  return reel