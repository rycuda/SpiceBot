import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('steenkin','dontneed')
def dontneed(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            bot.say(trigger.group(2) + "? weee dun neeeed no steenkin " + trigger.group(2) + "!!")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
