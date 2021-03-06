#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *


@thread(False)
@rule('(.*)')
@priority('low')
def antiflood(bot, trigger):
    instigator = trigger.nick
    if not trigger.is_privmsg and instigator != bot.nick and not bot.nick.endswith(devbot):
        ## vars
        channel = trigger.sender
        currentmessage = trigger.group(1)

        ## Flooding is 5 lines in a row by the same person or 3 identical lines
        floodyell = 0
        antifloodwarning = str(instigator + ", please do not flood the channel.")
        lastnicksubmit = get_botdatabase_value(bot, channel, 'automod_antifloodnick') or bot.nick
        if lastnicksubmit != instigator:
            set_botdatabase_value(bot, channel, 'automod_antifloodnick', instigator)
            set_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
            set_botdatabase_value(bot, channel, 'automod_antifloodnickwarned', None)
            set_botdatabase_value(bot, channel, 'automod_antifloodmessage', currentmessage)
            set_botdatabase_value(bot, channel, 'automod_antifloodmessagecount', 1)
        else:
            lastmessage = get_botdatabase_value(bot, channel, 'automod_antifloodmessage') or ''
            if currentmessage != lastmessage:
                set_botdatabase_value(bot, channel, 'automod_antifloodmessage', currentmessage)
                set_botdatabase_value(bot, channel, 'automod_antifloodmessagecount', 1)
            else:
                adjust_botdatabase_value(bot, channel, 'automod_antifloodmessagecount', 1)
                getcurrentmessagecount = get_botdatabase_value(bot, channel, 'automod_antifloodmessagecount') or 1
                if int(getcurrentmessagecount) >= 3:
                    floodyell = 1
            lastnicksubmit = get_botdatabase_value(bot, channel, 'automod_antifloodnick') or bot.nick
            adjust_botdatabase_value(bot, channel, 'automod_antifloodcount', 1)
            getcurrentcount = get_botdatabase_value(bot, channel, 'automod_antifloodcount') or 1
            if int(getcurrentcount) > 5:
                floodyell = 1
        lastnicksubmitwarned = get_botdatabase_value(bot, channel, 'automod_antifloodnickwarned') or bot.nick
        if lastnicksubmitwarned != instigator and floodyell:
            set_botdatabase_value(bot, channel, 'automod_antifloodnickwarned', instigator)
            bot.msg(channel,antifloodwarning)
