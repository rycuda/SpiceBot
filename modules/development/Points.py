#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import random
from random import randint
from sopel import module, tools
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('points','takepoints','pants','takepants','minuspants','minuspoints','checkpoints','checkpants')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    for c in bot.channels:
        channel = c
    commandused = trigger.group(1)
    inchannel = trigger.sender
    target = get_trigger_arg(triggerargsarray, 1) or trigger.nick
    if commandused.endswith('points'):
        pointstype = 'points'
    else:
        pointstype = 'pants'
    if commandused.startswith('check'):
        points = get_points(bot, target)
        if not points:
            bot.say(target + ' has no ' + pointstype + ' history.')
        else:
            bot.say(target + ' has ' + str(points) + ' ' + pointstype + '.')
    else:
        if commandused.startswith('take') or commandused.startswith('minus'):
            giveortake = ' takes '
            tofrom = ' from '
            addminus = 'down'
        else:
            giveortake = ' gives '
            tofrom = ' to '
            addminus = 'up'      
        return pointstask(bot, channel, trigger.nick, trigger.group(3) or '', giveortake, tofrom, addminus, pointstype, inchannel)

def pointstask(bot, channel, instigator, target, giveortake, tofrom, addminus, pointstype, inchannel):
    target = tools.Identifier(target or '')
    rando = randint(1, 666)
    randopoints = (instigator + str(giveortake) + str(rando) + ' ' + pointstype + str(tofrom) + ' ')    
    if not target:
        bot.say(str(randopoints) + "everyone")
        channelpoints(bot, instigator, channel, rando, addminus)
    else:
        if target == 'all' or target == 'everybody' or target == 'everyone':
            if not inchannel.startswith("#"):
                bot.say('you must be in the room to give everyone points')
            else:
                bot.say(str(randopoints) + "everyone")
                channelpoints(bot, instigator, channel, rando, addminus)
        elif target == instigator:
            bot.say('You can\'t adjust your own ' + pointstype + '!!')
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            bot.say(str(randopoints) + target)
            update_points(bot, target, rando, addminus)
            if target != instigator and not inchannel.startswith("#"):
                bot.notice(str(randopoints) + target, target)
            
def channelpoints(bot, instigator, channel, rando, addminus):
    for u in bot.channels[channel].users:
        errrbody = u
        if errrbody != instigator:
            update_points(bot, errrbody, rando, addminus)
            
def update_points(bot, nick, rando, addminus):
    pointsgotten = get_points(bot, nick)
    if addminus == 'up':
        bot.db.set_nick_value(nick, 'points_points', pointsgotten + int(rando))
    else:
        bot.db.set_nick_value(nick, 'points_points', pointsgotten - int(rando))

def get_points(bot, nick):
    points = bot.db.get_nick_value(nick, 'points_points') or 1
    return points