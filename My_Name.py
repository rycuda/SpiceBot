import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('spicebot','spicebotdev')
def name(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say("That's my name. Don't wear it out!")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
