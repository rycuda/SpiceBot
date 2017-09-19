import sopel.module
from sopel.tools.target import User, Channel

@sopel.module.commands('getchannels')
def getChannels(bot,trigger):
	for c in bot.channels:
		bot.say("You can find me in " + c)
@sopel.module.commands('getmembers')
def getMembers(bot,trigger):
    #users = str(bot.channels[trigger.sender].users)
    #bot.say(users)
    for u in bot.channels[trigger.sender].users:
        bot.say(u)
@sopel.module.commands('dbtest')
def get_duels(bot, trigger):
    wins = bot.db.get_nick_value(trigger.nick, 'duel_wins') or 0
    losses = bot.db.get_nick_value(trigger.nick, 'duel_losses') or 0
    bot.say(str(wins))
    bot.say(str(losses))
