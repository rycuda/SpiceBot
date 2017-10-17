import json
import re
import urllib
import sopel.module
from sopel import module

@sopel.module.rate(120)

def format_defn(defn, num, max):
    lines = []
    pieces = re.split(r'\n+', defn['definition'])
    lines.append('%s: definition %i of %i' % (defn['word'], num, max))
    lines.extend(pieces)
    lines.append('Example: %s' % defn['example'].split('\n')[0])
    return lines

def urban(bot, input):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        baseurl = 'http://api.urbandictionary.com/v0/'

        if not input.group(2):
            bot.say('Usage: .urban <word> [definition number]')
            return

        input = input.group(2).strip()
        words = input.split()
        try:
            num = int(words[-1])
            input = ' '.join(words[:-1])
        except ValueError:
            num = 1

        if input == 'random':
            url = baseurl + 'random'
        else:
            url = baseurl + 'define?term=' + input

        try:
            result = json.loads(urllib.urlopen(url).read())
        except:
            return

        if not result or "list" not in result:
            return

        idx = num - 1
        max = len(result['list'])
        try:
            defn = result['list'][idx]
        except IndexError:
            bot.say('No definition %i of %i for %s' % (idx, max, input))
            return

        lines = format_defn(defn, num, max)
        for line in lines:
            bot.say(line)
    urban.commands = ['urban']


    if __name__ == '__main__':
        import sys

        class Sopel(object):
            def say(self, msg):
                print msg

        urban(Sopel(), re.match('()(.*)', sys.argv[1]))
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
