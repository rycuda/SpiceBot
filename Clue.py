import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('clue')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)

rooms = ['Ballroom', 'Billiard Room', 'Cellar', 'Conservatory', 'Dining Room', 'Kitchen', 'Hall', 'Library', 'Lounge', 'Study']
weapons = ['Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'RopeCandlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench', 'Wrench']
    
def execute_main(bot, trigger):
    players = []
    for c in bot.channels:
        channel = c
    for u in bot.channels[channel].users:
        target = u
        if get_spicebotdisenable(bot, target):
            players.append(target)
    random.shuffle(rooms)
    random.shuffle(weapons)
    random.shuffle(players)
    bot.say(players[0] + " killed " + players[1] + " in the " + rooms[0] + " with the " + weapons[0] + ".")