import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('gif','giphy')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):       
    if trigger.group(2):
        query = trigger.group(2).replace(' ', '%20')
        query = str(query)
        gif,randno = getGif(query)
        if gif:
            bot.say("Result number " + str(randno) + ": " + gif)
        else:
            bot.say('Hmm...Couldn\'t find a gif for that!')
    else:
        bot.say('Tell me what you\'re looking for!')
            
def getGif(query):
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    limit = 50
    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(query)+'&api_key=' + str(api) + '&limit=' + str(limit) + '&rating=r'    
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0,limit)
    try:
        id = data['data'][randno]['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except IndexError:
        gif = ""
    return gif,randno
