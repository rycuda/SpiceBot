import sopel.module
from sopel import module, tools

@module.require_chanmsg
@sopel.module.commands('spiceboton','spicebotoff')
def isshelistening(bot,trigger):
    channel = trigger.sender
    target = trigger.group(3) or trigger.nick
    commandtrimmed = trigger.group(1)
    commandtrimmed = str(commandtrimmed.split("spicebot", 1)[1])
    if not trigger.admin and target != trigger.nick:
        bot.say("Only bot admins can mark other users ability to use " + bot.nick + ".")
    elif target.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")
    elif target = 'all' and commandtrimmed == 'off':
        for u in bot.channels[channel].users:
            target = u
            disenable = get_disenable(bot, target)
            if disenable:
                bot.db.set_nick_value(target, 'spicebot_disenable', '')
    else:
        disenable = get_disenable(bot, target)
        if commandtrimmed == 'on':
            if not disenable:
                bot.db.set_nick_value(target, 'spicebot_disenable', 'true')
                bot.say(bot.nick + ' has been enabled for ' + target)
            else:
                bot.say(bot.nick + ' is already enabled for ' + target)
        elif commandtrimmed == 'off':
            if not disenable:
                bot.say(bot.nick + ' is already disabled for ' + target)
            else:
                bot.db.set_nick_value(target, 'spicebot_disenable', '')
                bot.say(bot.nick + ' has been disabled for ' + target)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
