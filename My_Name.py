import sopel.module

def getbotnick():
    botnick = bot.nick
    return botnick

@sopel.module.commands(botnick)
def name(bot,trigger):
    bot.say("That's my name. Don't wear it out!")


