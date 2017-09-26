import sopel.module
from sopel.module import ADMIN
from sopel.tools.target import User, Channel

@sopel.module.commands('isadmin')
def isadmin(bot,trigger):
    if not trigger.group(2):
        nick = trigger.nick.lower()
    else:
        nick = trigger.group(2).lower()
    try:    
        if bot.privileges[trigger.sender][nick].admin:
            bot.say(nick + ' is an admin.')
        else: 
            bot.say(nick + ' is not an admin.')
    except KeyError:
        bot.say(nick + ' is not here right now!')

@sopel.module.commands('getpriv')
def getpriv(bot,trigger):
    for p in bot.privileges:
        bot.say(c)
