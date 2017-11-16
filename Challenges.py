import sopel.module
import sopel
from sopel import module, tools
import random
from random import randint
import time
import re
import sys
import os
from os.path import exists
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## Configurables #############
TIMEOUT = 180
TIMEOUTC = 40
ALLCHAN = 'entirechannel'
OPTTIMEOUT = 1800
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
challengestatsadminarray = ['wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','disenable','poisonpotion','manapotion','lastfought','konami']
challengestatsarray = ['health','mana','xp','wins','losses','winlossratio','respawns','kills','backpackitems','lastfought','timeout']

####################
## Main Operation ##
####################

@sopel.module.commands('challenge','duel')
def challenge_cmd(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        return mainfunction(bot, trigger)
        
def mainfunction(bot, trigger):
    
    ## Basic Vars that we will use
    instigator = trigger.nick
    inchannel = trigger.sender
    fullcommandused = trigger.group(2)
    commandortarget = trigger.group(3)
    for c in bot.channels:
        channel = c
    now = time.time()
    
    ## Make sure Opt-In time is there
    opttime = get_database_value(bot, instigator, 'opttime')
    if not opttime:
        set_database_value(bot, instigator, 'opttime', now)
    
    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who did you want to challenge? Online Docs: https://github.com/deathbybandaid/sopel-modules/blob/master/otherfiles/ChallengesDocumentation.md", instigator)
    
    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() not in bot.privileges[channel.lower()]:
        commandused = trigger.group(3)
        target = trigger.group(4)
        if not target:
            target = trigger.nick
        targetdisenable = get_database_value(bot, target, 'disenable')
        
        ## Arrays
        nontargetarray = ['everyone','add','del','inv','health','attack','instakill']
        adminonlyarray = ['statsadmin']
        privilegedarray = ['on','off']
        
        ## Must clear these4 challenges to do the below functions
        if target.lower() not in bot.privileges[channel.lower()] and target not in nontargetarray:
            bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
        elif not trigger.admin and commandused in adminonlyarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif target != instigator and not trigger.admin and commandused in privilegedarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif not targetdisenable and target != instigator and commandused != 'on' and commandused != 'off' and target not in nontargetarray:
            bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
        elif target == bot.nick:
            bot.notice(instigator + " I cannot do that.", instigator)
            
        ## and, continue
        else:
            targetopttime = get_database_value(bot, target, 'opttime')
            targetopttime = abs(now - targetopttime)
            targetopttimemath = (OPTTIMEOUT - targetopttime)
            lastfought = get_database_value(bot, instigator, 'lastfought')
                    
            ## Docs
            if commandused == 'docs' or commandused == 'help':
                bot.say("Online Docs: https://github.com/deathbybandaid/sopel-modules/blob/master/otherfiles/ChallengesDocumentation.md")
            
            ## Random Dueling
            elif commandused == 'random':
                if not lastfought:
                    lastfought = instigator
                randomtargetarray = []
                for u in bot.channels[channel].users:
                    target = u
                    if target != instigator and target != bot.nick:
                        if target != lastfought or bot.nick.endswith('dev'):
                            targetdisenable = get_database_value(bot, target, 'disenable')
                            targettime = get_timesince(bot, target)
                            targetspicebotdisenable = get_spicebotdisenable(bot, target)
                            if targetdisenable and targettime > TIMEOUT and targetspicebotdisenable or bot.nick.endswith('dev'):
                                randomtargetarray.append(target)
                if randomtargetarray == []:
                    bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
                else:
                    randomselected = random.randint(0,len(randomtargetarray) - 1)
                    target = str(randomtargetarray [randomselected])
                    return getreadytorumble(bot, trigger, instigator, target)

            ## On/off
            elif commandused == 'on' or commandused == 'off':
                disenablevalue = ''
                if commandused == 'on':
                    disenablevalue = 1
                if target == 'everyone':
                    for u in bot.channels[channel].users:
                        target = u
                        set_database_value(bot, target, 'disenable', disenablevalue)
                elif targetopttime < OPTTIMEOUT and not bot.nick.endswith('dev'):
                    bot.notice(instigator + ", It looks like " + target + " can't enable/disable challenges for " + str(targetopttimemath) + " seconds.", instigator)
                else:
                    if targetdisenable and commandused == 'on':
                        bot.notice(instigator + ", It looks like " + target + " already has duels on.", instigator)
                    elif not targetdisenable and commandused == 'off':
                        bot.notice(instigator + ", It looks like " + target + " already has duels off.", instigator)
                    else:
                        set_database_value(bot, target, 'disenable', disenablevalue)
                        set_database_value(bot, target, 'opttime', now)
                        bot.notice(instigator + ", It looks like Challenges should be " +  commandused + ' for ' + target + '.', instigator)

            ## Stats
            elif commandused == 'stats':
                stats = ''
                for x in challengestatsarray:
                    if x == 'winlossratio' or x == 'backpackitems':
                        scriptdef = str('get_' + x + '(bot,target)')
                        gethowmany = eval(scriptdef)
                    else:
                        gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    stats = str(target + "'s stats:" + stats)
                    bot.notice(stats, instigator)
                else:
                    bot.notice(instigator + ", It looks like " + target + " has no stats.", instigator)

            ## Backpack
            elif commandused == 'backpack':
                backpack = ''
                for x in lootitemsarray:
                    gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        addbackpack = str(' ' + str(x) + "=" + str(gethowmany))
                        backpack = str(backpack + addbackpack)
                if backpack != '':
                    backpack = str(target + "'s backpack:" + backpack)
                    bot.notice(backpack, instigator)
                else:
                    bot.notice(instigator + ", It looks like " + target + " has no backpack items.", instigator)

            ## Stats Admin
            elif commandused == 'statsadmin' and trigger.admin:
                statsadminarray = ['set','reset']
                commandtrimmed = trigger.group(5)
                statset = trigger.group(6)
                newvalue = str(fullcommandused.split(statset, 1)[1]).strip()
                if commandtrimmed not in statsadminarray:
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                elif statset not in challengestatsadminarray and statset != 'all':
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                elif commandtrimmed == 'set' and not newvalue:
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                else:
                    if not newvalue:
                        newvalue = ''
                    if target == 'everyone':
                        for u in bot.channels[channel].users:
                            etarget = u
                            if statset == 'all':
                                for x in challengestatsadminarray:
                                    estatset = x
                                    databasecolumn = str('challenges_' + estatset)
                                    bot.db.set_nick_value(etarget, databasecolumn, newvalue)
                            else:
                                databasecolumn = str('challenges_' + statset)
                                bot.db.set_nick_value(target, databasecolumn, newvalue)
                    else:
                        if statset == 'all':
                            for x in challengestatsadminarray:
                                statset = x
                                databasecolumn = str('challenges_' + statset)
                                bot.db.set_nick_value(target, databasecolumn, newvalue)
                        else:
                            databasecolumn = str('challenges_' + statset)
                            bot.db.set_nick_value(target, databasecolumn, newvalue)
                    bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)

            ## Leaderboard
            elif commandused == 'leader':
                currentleader = ''
                currentleadernumber = 0
                for u in bot.channels[channel].users:
                    target = u
                    targetdisenable = get_database_value(bot, target, 'disenable')
                    if targetdisenable:
                        winlossratio = get_winlossratio(bot,target)
                        if winlossratio > currentleadernumber:
                            currentleader = target
                            currentleadernumber = winlossratio
                leaderboardscript = str("The Current Leader in the room is: " + str(currentleader) + " with a ratio of: " + str(currentleadernumber))
                bot.say(leaderboardscript)
            
            ## Close to death
            elif commandused == 'closetodeath':
                currentleader = ''
                currentleadernumber = 9999999999
                for u in bot.channels[channel].users:
                    target = u
                    targetdisenable = get_database_value(bot, target, 'disenable')
                    if targetdisenable:
                        health = get_database_value(bot, target, 'health')
                        if health < currentleadernumber:
                            currentleader = target
                            currentleadernumber = health
                leaderboardscript = str("The Current person close to death in the room is: " + str(currentleader) + " with health at: " + str(currentleadernumber))
                bot.say(leaderboardscript)
                    
            ## Loot Items usage
            elif commandused in lootitemsarray:
                uselootitem = 0
                gethowmany = get_database_value(bot, instigator, commandused)
                if gethowmany:
                    saymsg = 'true'
                    use_lootitem(bot, instigator, target, inchannel, commandused, saymsg)
                else:
                    bot.notice(instigator + ", You do not have a " +  commandused + " to use!", instigator)
         
            ## Konami
            elif commandused == 'upupdowndownleftrightleftrightba':
                konami = get_database_value(bot, target, 'konami')
                if not konami:
                    set_database_value(bot, instigator, 'konami', 1)
                    bot.notice(instigator + " you have found the cheatcode easter egg!!!", instigator)
                else:
                    bot.notice(instigator + " you can only cheat once.", instigator)
                
            ## Weaponslocker
            elif commandused == 'weaponslocker':
                weaponslist = get_weaponslocker(bot, instigator)
                adjustmentdirection = trigger.group(4)
                if not adjustmentdirection:
                    bot.say('Use .duel weaponslocker add/del to adjust Locker Inventory.')
                elif adjustmentdirection == 'inv' and not inchannel.startswith("#"):
                    weaponslistnew = []
                    for weapon in weaponslist:
                        weapon = str(weapon)
                        weaponslistnew.append(weapon)
                    for channel in bot.channels:
                        bot.db.set_nick_value(channel, 'weapons_locker', '')
                    for weapon in weaponslistnew:
                        if weapon not in weaponslist:
                            weaponslist.append(weapon)
                    update_weaponslocker(bot, instigator, weaponslist)
                    weaponslist = get_weaponslocker(bot, instigator)
                    weaponslist = str(weaponslist)
                    weaponslist = weaponslist.replace('[', '')
                    weaponslist = weaponslist.replace(']', '')
                    weaponslist = weaponslist.replace("u'", '')
                    weaponslist = weaponslist.replace('u"', '')
                    weaponslist = weaponslist.replace("'", '')
                    weaponslist = weaponslist.replace('"', '')
                    chunks = weaponslist.split()
                    per_line = 15
                    for i in range(0, len(chunks), per_line):
                        weaponline = " ".join(chunks[i:i + per_line])
                        bot.say(str(weaponline))
                elif adjustmentdirection == 'inv' and inchannel.startswith("#"):
                    bot.say('Inventory can only be viewed in privmsg.')
                else:
                    weaponchange = str(fullcommandused.split(adjustmentdirection, 1)[1]).strip()
                    if not weaponchange:
                        bot.say("What weapon would you like to add/remove?")
                    else:
                        if weaponchange in weaponslist:
                            if adjustmentdirection == 'add':
                                weaponlockerstatus = 'already'
                            else:
                                weaponslist.remove(weaponchange)
                                update_weaponslocker(bot, instigator, weaponslist)
                                weaponlockerstatus = 'no longer'
                        else:
                            if adjustmentdirection == 'add':
                                weaponslist.append(weaponchange)
                                update_weaponslocker(bot, instigator, weaponslist)
                                weaponlockerstatus = 'now'
                            else:
                                weaponlockerstatus = 'already not'
                        message = str(weaponchange + " is " + weaponlockerstatus + " in your weapons locker.")
                        bot.say(message)
        
            ## Magic Attack
            elif commandused == 'magic':
                magicoptions = ['attack','instakill','health']
                magicusage = trigger.group(4)
                if magicusage not in magicoptions:
                    bot.say('Magic uses include: attack, instakill, health')
                else:
                    target = trigger.group(5)
                    if not target:
                        target = trigger.nick
                    mana = get_database_value(bot, instigator, 'mana')
                    if magicusage == 'attack':
                        manarequired = -250
                        damage = -200
                    elif magicusage == 'health':
                        manarequired = -200
                        damage = 200
                    elif magicusage == 'instakill':
                        manarequired = -1000
                        damage = -99999
                    if not mana:
                        bot.notice(instigator + " you don't have any mana.", instigator)
                    elif mana < manarequired:
                        manamath = int(manarequired - mana)
                        bot.notice(instigator + " you need " + str(manamath) + " more mana to do this attack.", instigator)
                    else:
                        if target.lower() not in bot.privileges[channel.lower()]:
                            bot.say("I'm not sure who that is.")
                        else:
                            targethealthstart = get_database_value(bot, target, 'health')
                            adjust_database_value(bot, instigator, 'mana', manarequired)
                            adjust_database_value(bot, target, 'health', damage)
                            targethealth = get_database_value(bot, target, 'health')
                            if targethealth <= 0:
                                update_respawn(bot, target)
                                set_database_value(bot, target, 'opttime', now)
                                adjust_database_value(bot, instigator, 'kills', '1')
                                lootcorpse(bot, target, instigator)
                                magicsay = str(instigator + ' uses magic on ' + target + ', killing ' + target)
                                magicnotice = str(instigator + " used a magic on you that killed you")
                            elif magicusage == 'health':
                                healthmath = int(int(targethealth) - int(targethealthstart))
                                magicsay = str(instigator + ' uses magic on ' + target + ' that increased health by ' + str(healthmath))
                                magicnotice = str(instigator + " used a magic on you that increased health by " + str(healthmath))
                            else:
                                magicsay = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damage) + ' damage.')
                                magicnotice = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damage) + ' damage.')
                            bot.say(str(magicsay))
                            if not inchannel.startswith("#") and target != instigator:
                                bot.notice(str(magicnotice), target)
                                
            else:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
    else:
        lastfought = get_database_value(bot, instigator, 'lastfought')
        target = trigger.group(3)
        targetspicebotdisenable = get_spicebotdisenable(bot, target)
        instigatordisenable = get_database_value(bot, instigator, 'disenable')
        targetdisenable = get_database_value(bot, target, 'disenable')
        instigatortime = get_timesince(bot, instigator)
        targettime = get_timesince(bot, target)
        channeltime = get_timesince(bot, ALLCHAN)
        if not inchannel.startswith("#"):
            bot.notice(instigator + " Duels must be in channel.", instigator)
        elif target == bot.nick:
            bot.notice(instigator + " I refuse to fight a biological entity!", instigator)
        elif target == instigator:
            bot.notice(instigator + " If you are feeling self-destructive, there are places you can call.", instigator)
        elif target == lastfought and not bot.nick.endswith('dev'):
            bot.notice(instigator + ', You may not fight the same person twice in a row.', instigator)
        elif not targetspicebotdisenable:
            bot.notice(instigator + ', It looks like ' + target + ' has disabled Spicebot.', instigator)
        elif not instigatordisenable:
            bot.notice(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.", instigator)
        elif not targetdisenable:
            bot.notice(instigator + ', It looks like ' + target + ' has disabled Challenges.', instigator)
        elif instigatortime < TIMEOUT and not bot.nick.endswith('dev'):
            bot.notice("You can't challenge for %d seconds." % (TIMEOUT - instigatortime), instigator)
            if targettime < TIMEOUT:
                bot.notice(target + " can't challenge for %d seconds." % (TIMEOUT - targettime), instigator)
            if channeltime < TIMEOUTC:
                bot.notice(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime), instigator)
        elif targettime < TIMEOUT and not bot.nick.endswith('dev'):
            bot.notice(target + " can't challenge for %d seconds." % (TIMEOUT - targettime), instigator)
            if channeltime < TIMEOUTC:
                bot.notice(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime), instigator)
            elif channeltime < TIMEOUTC and not bot.nick.endswith('dev'):
                bot.notice(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime), instigator)
        else:
            return getreadytorumble(bot, trigger, instigator, target)
        
def getreadytorumble(bot, trigger, instigator, target):
    ## Vars
    fullcommandused = trigger.group(2)
    targetsplit = trigger.group(3)
    now = time.time()
    
    ## Announce Combat
    announcecombatmsg = str(instigator + " versus " + target)
       
    ## Check new player health
    instigatorhealth = get_database_value(bot, instigator, 'health')
    if not instigatorhealth:
        set_database_value(bot, instigator, 'health', '1000')
    targethealth = get_database_value(bot, target, 'health')
    if not targethealth:
        set_database_value(bot, target, 'health', '1000')

    ## Damage Done
    damage = damagedone(bot)

    ## Select Winner
    winner, loser = getwinner(bot, instigator, target)

    ## Weapon Select
    weapon = str(fullcommandused.split(targetsplit, 1)[1]).strip()
    if not weapon or winner == target:
        weapon = weaponofchoice(bot, winner)
    weapon = weaponformatter(bot, weapon)
           
    ## Update Wins and Losses
    adjust_database_value(bot, winner, 'wins', '1')
    adjust_database_value(bot, loser, 'losses', '1')
            
    ## Update XP points
    XPearnedwinner = '5'
    XPearnedloser = '3'
    adjust_database_value(bot, winner, 'xp', XPearnedwinner)
    adjust_database_value(bot, loser, 'xp', XPearnedloser)
                
    ## Update last fought
    set_database_value(bot, instigator, 'lastfought', target)
    set_database_value(bot, target, 'lastfought', instigator)
            
    ## Update Health Of Loser, respawn, allow winner to loot
    adjust_database_value(bot, loser, 'health', damage)
    damage = abs(damage)
    currenthealth = get_database_value(bot, loser, 'health')
    if currenthealth <= 0:
        winnermsg = str(winner + ' killed ' + loser + " with " + weapon + ' forcing a respawn!!')
        update_respawn(bot, loser)
        set_database_value(bot, loser, 'mana', '')
        adjust_database_value(bot, winner, 'kills', '1')
        ## Loot Corpse
        lootcorpse(bot, loser, winner)
    else:
        winnermsg = str(winner + " hits " + loser + " with " + weapon + ', dealing ' + str(damage) + ' damage.')
            
    ## Random Inventory gain
    lootwinnermsg = ''
    lootwinnermsgb = ''
    randominventoryfind = randominventory()
    if randominventoryfind == 'true':
        loot = determineloottype(bot, winner)
        loot_text = get_lootitem_text(bot, winner, loot)
        adjust_database_value(bot, winner, loot, '1')
        lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
        if winner == target:
            lootwinnermsgb = str(winner + " gains the " + str(loot))
                               
    ## On Screen Text
    bot.say(str(announcecombatmsg) + "       " + str(lootwinnermsg))
    bot.say(str(winnermsg)+ "       " + str(lootwinnermsgb))
        
    ## Update Time Of Combat
    set_database_value(bot, instigator, 'timeout', now)
    set_database_value(bot, target, 'timeout', now)
    set_database_value(bot, ALLCHAN, 'timeout', now)

## Health Regeneration
@sopel.module.interval(1800)
def healthregen(bot):
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            target = u
            targetdisenable = get_database_value(bot, target, 'disenable')
            if targetdisenable:
                health = get_database_value(bot, target, 'health')
                if health < 500:
                    bot.db.set_nick_value(target, 'challenges_health', int(health) + 50)
        
## Functions######################################################################################################################

## Database
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('challenges_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey)
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))
    
##########
## Time ##
##########
    
def get_timesince(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'challenges_timeout') or 0
    return abs(now - int(last))
    
#####################
## Spawn / ReSpawn ##
#####################

def update_respawn(bot, nick):
    respawns = get_database_value(bot, nick, 'respawns')
    bot.db.set_nick_value(nick, 'challenges_respawns', respawns + 1)
    bot.db.set_nick_value(nick, 'challenges_health', '1000')
    currentrespawns = get_database_value(bot, nick, 'respawns')
    return currentrespawns
    
###############
## Inventory ##
###############

def get_backpackitems(bot, target):
    totalbackpack = 0
    for x in lootitemsarray:
        gethowmany = get_database_value(bot, target, x)
        totalbackpack = int(int(totalbackpack) + int(gethowmany))
    return totalbackpack

## maybe add a dice roll later
def randominventory():
    randomfindchance = randint(1, 120)
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    else:
        randominventoryfind = 'false'
    return randominventoryfind

def determineloottype(bot, nick): 
    loot = random.randint(0,len(lootitemsarray) - 1)
    loot = str(lootitemsarray [loot])
    return loot

def lootcorpse(bot, loser, winner):
    for x in lootitemsarray:
        gethowmany = get_database_value(bot, loser, x)
        if gethowmany:
            set_database_value(bot, target, x, '')
            gethowmanyb = get_database_value(bot, winer, x)
            set_database_value(bot, target, x, int(gethowmany) + int(gethowmanyb))

def get_lootitem_text(bot, nick, loottype):
    if loottype == 'healthpotion':
        loot_text = ': worth 100 health.'
    elif loottype == 'poisonpotion':
        loot_text = ': worth -50 health.'
    elif loottype == 'manapotion':
        loot_text = ': worth 100 mana.'
    elif loottype == 'timepotion':
        loot_text = ': worth up to ' + str(TIMEOUT) + ' seconds of timeout.'
    elif loottype == 'mysterypotion':
        loot_text = ': With unknown effects!'
    else:
        loot_text = ''
    if loot_text != '':
        loot_text = str(loot_text + " Use .challenge " + str(loottype) + " to consume.")
    return loot_text
        
def use_lootitem(bot, instigator, target, inchannel, loottype, saymsg):
    bot.say(loottype)
    targethealth = get_database_value(bot, target, 'health')
    if not targethealth:
        set_database_value(bot, target, 'health', '1000')
        health = get_database_value(bot, target, 'health')
    gethowmany = get_database_value(bot, target, 'mana')
    adjust_database_value(bot, instigator, loottype, -1)
    mana = get_database_value(bot, target, 'mana')
    if target == instigator:
        mainlootusemessage = str(instigator + ' uses ' + loottype + '.')
    else:
        mainlootusemessage = str(instigator + ' uses ' + loottype + ' on ' + target + ". ")
    if loottype == 'healthpotion':
        adjust_database_value(bot, target, 'health', '100')
    elif loottype == 'posionpotion':
        adjust_database_value(bot, target, 'health', '-50')
    elif loottype == 'manapotion':
        adjust_database_value(bot, target, 'mana', '100')
    elif loottype == 'timepotion':
        set_database_value(bot, target, 'timeout', '')
    elif loottype == 'mysterypotion':
        loot = random.randint(0,len(lootitemsarray) - 1)
        loot = str(lootitemsarray [loot])
        if loot != 'mysterypotion':
            adjust_database_value(bot, instigator, loot, '1')
            saymsg = 'false'
            use_lootitem(bot, instigator, target, inchannel, loot, saymsg)
            saymsg = 'true'
            lootusemsg = str("a " + loot)
        else:
            nulllootitemsarray = ['water','vinegar','mud']
            nullloot = random.randint(0,len(nulllootitemsarray) - 1)
            nullloot = str(nulllootitemsarray [nullloot])
            bot.say('Looks like the Potion was just ' + str(nullloot) + ' after all.')
            lootusemsg = str("Just " + nullloot)
        mainlootusemessage = str(mainlootusemessage + ' It was ' + str(lootusemsg) + '. ')
    else:
        mainlootusemessage = str(mainlootusemessage + '')
    health = get_database_value(bot, target, 'health')
    if targethealth <= 0:
        mainlootusemessage = str(mainlootusemessage + "This resulted in death.")
        update_respawn(bot, target)
        set_database_value(bot, target, 'mana', '')
        adjust_database_value(bot, instigator, 'kills', '1')
        lootcorpse(bot, target, instigator)
    if saymsg == 'true':
        bot.say(str(mainlootusemessage))
        if not inchannel.startswith("#") and target != instigator:
            bot.notice(str(mainlootusemessage), target)
    
######################
## Weapon Selection ##
######################

def weaponofchoice(bot, nick):
    weaponslist = get_weaponslocker(bot, nick)
    if weaponslist == []:
        weapon = "fist"
    else:
        weaponselected = random.randint(0,len(weaponslist) - 1)
        weapon = str(weaponslist [weaponselected])
    return weapon

def weaponformatter(bot, weapon):
    if weapon.lower().startswith('a ') or weapon.lower().startswith('an ') or weapon.lower().startswith('the '):
        weapon = str(weapon)
    elif weapon.lower().startswith('a') or weapon.lower().startswith('e') or weapon.lower().startswith('i') or weapon.lower().startswith('o') or weapon.lower().startswith('u'):
        weapon = str('an ' + weapon)
    else:
        weapon = str('a ' + weapon)
    return weapon

#################
## Damage Done ##
#################

def damagedone(bot):
    rando = randint(1, 100)
    if rando >= 90:
        damage = -120
    elif rando >= 75 and rando < 90:
        damage = -70
    elif rando < 75 and rando > 10:
        damage = -40
    elif rando > 1 and rando <= 10:
        damage = -10 
    else:
        damage = -5
    return damage

###################
## Select Winner ##
###################

def getwinner(bot, instigator, target):
    instigatorxp = get_database_value(bot, instigator, 'xp')
    if not instigatorxp:
        instigatorxp = '1'
    targetxp = get_database_value(bot, target, 'xp')
    if not targetxp:
        targetxp = '1'
    
    ## each person
    instigatorfight = '1'
    targetfight = '1'

    # instigator gets 1 for surprise
    instigatorfight = int(instigatorfight) + 1

    # XP difference
    if int(instigatorxp) > int(targetxp):
        instigatorfight = int(instigatorfight) + 1
    elif int(instigatorxp) < int(targetxp):
        targetfight = int(targetfight) + 1
    elif int(instigatorxp) == int(targetxp):
        instigatorfight = int(instigatorfight) + 1
        targetfight = int(targetfight) + 1
    else:
        instigatorfight = int(instigatorfight) + 1
        targetfight = int(targetfight) + 1
        
    ## Random Number
    flip = randint(0, 1)
    if (flip == 0):
        instigatorfight = int(instigatorfight) + 1
    else:
        targetfight = int(targetfight) + 1
    
    ## Dice Roll
    instigatorfightarray = []
    targetfightarray = []
    while int(instigatorfight) > 0:
        instigatorfightroll = diceroll()
        instigatorfightarray.append(instigatorfightroll)
        instigatorfight = int(instigatorfight) - 1
    instigatorfight = max(instigatorfightarray)
    while int(targetfight) > 0:
        targetfightroll = diceroll()
        targetfightarray.append(targetfightroll)
        targetfight = int(targetfight) - 1
    targetfight = max(targetfightarray)
 
    ## tie breaker
    if instigatorfight == targetfight:
        tiebreaker = randint(0, 1)
        if (tiebreaker == 0):
            instigatorfight = int(instigatorfight) + 1
        else:
            targetfight = int(targetfight) + 1
            
    ## Compare
    if int(instigatorfight) > int(targetfight):
        winner = instigator
    else:
        winner = target
        
    ## LOSER IS NOT WINNER
    if winner == instigator:
        loser = target
    else:
        loser = instigator
    return winner, loser

###############
## ScoreCard ##
###############

def get_winlossratio(bot,target):
    wins = get_database_value(bot, target, 'wins')
    wins = int(wins)
    losses = get_database_value(bot, target, 'losses')
    losses = int(losses)
    if not wins and not losses:
        winlossratio = 0
    else:
        winlosstotal = abs(wins + losses)
        if winlosstotal != 0:
            winlossratio = float(wins)/winlosstotal
        else:
            winlossratio = 0
    return winlossratio

####################
## Weapons Locker ##
####################

def get_weaponslocker(bot, nick):
    for channel in bot.channels:
        weaponslist = bot.db.get_nick_value(nick, 'weapons_locker') or []
        return weaponslist

def update_weaponslocker(bot, nick, weaponslist):
    for channel in bot.channels:
        bot.db.set_nick_value(nick, 'weapons_locker', weaponslist)

###########
## Tools ##
###########

def diceroll():
    diceroll = randint(0, 20)
    return diceroll
