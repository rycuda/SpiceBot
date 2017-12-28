#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import datetime
from sopel import module, tools
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

 
@sopel.module.commands('spicebucks')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, args):
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = special_users(bot)
    #for c in bot.channels:
        #channel = c
    #commandused = trigger.group(3)
    #inchannel = trigger.sender
    if len(args) == 0:
        bot.say("Welcome to the #Spiceworks Bank.  Your options are payday and bank.")
    elif len(args) >= 1:
		if args[0] == 'payday':  
			paydayamount=checkpayday(bot, trigger.nick, args[0])
			if paydayamount > 0:
				spicebucks(bot, target, 'plus', paydayamount)
				bot.say("You haven't been paid yet today. Here's your " + str(paydayamount) + " spicebucks.")
			else:
				bot.say("You've already been paid today. Now go do some work.")
			
		elif args[0] == 'makeitrain':
	 		if not args[1]:
				bot.say('Spicebucks rain on ' + trigger.nick)
			else:
				if args[1] not in allusersinroomarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
				else:
					bot.say('Spicebucks rain on ' + args[1])
		
		elif args[0] == 'reset': #admin only command
			if trigger.nick not in adminsarray:
				bot.say('You must be an admin to use this command')
			else:
				if not args[1]:
					reset(bot,trigger.nick)
					bot.say('Payday reset for ' + trigger.nick)
				else:
					if args[1] not in allusersinroomarray:
						bot.say("I'm sorry, I do not know who " + args[1] + " is.")
					else:
						reset(bot,arg[1])
						bot.say('Payday reset for ' + arg[1])
                        
                
		elif args[0] == 'taxes':
			if len(args) > 1:
				if args[1] not in allusersinroomarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
				else:
					paytaxes(bot, args[1])
			else:
				paytaxes(bot, trigger.nick)
		elif args[0] == 'bank':
			if len(args) > 1:
				if args[1] not in allusersinroomarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
				else:
					spicebucks=bank(bot, args[1])                                         
					bot.say(args[1] + ' has '+ str(spicebucks) + " spicebucks in the bank.")
			else:
				spicebucks=bank(bot, trigger.nick)
				bot.say("You have " + str(spicebucks) + " spicebucks in the bank.")       
                     
		elif args[0] == 'transfer':
			if len(args) >= 3:
				transfer(bot, allusersinroomarray, trigger.nick, args[1], args[2])
			else:
				bot.say("You must enter who you would like to transfer spicebucks to, as well as an amount.")
            
def reset(bot, target): ##### to be removed, verify payday
    bot.db.set_nick_value(target, 'spicebucks_payday', 0)
    
def bank(bot, nick):
    spicebucks = bot.db.get_nick_value(nick, 'spicebucks_bank') or 0
    return spicebucks

def spicebucks(bot, target, plusminus, amount):
	#command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bot.db.get_nick_value(target, 'spicebucks_bank') or 0
        if plusminus == 'plus':
			bot.db.set_nick_value(target, 'spicebucks_bank', inbank + amount)
			success = 'true'
        elif plusminus == 'minus':
            if inbank - amount < 0:
                #bot.say("I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
                success = 'false'
            else:
                bot.db.set_nick_value(target, 'spicebucks_bank', inbank - amount)
                success = 'true'            
    else:
        #bot.say("The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success #returns simple true or false so modules can check the if tranaction was a success
    
    
def checkpayday(bot, target, args):
	paydayamount=0
	now = datetime.datetime.now()
	datetoday = int(now.strftime("%Y%j"))
	lastpayday = bot.db.get_nick_value(target, 'spicebucks_payday') or 0
	if lastpayday == 0 or lastpayday < datetoday:
		paydayamount = 15
		bot.db.set_nick_value(target, 'spicebucks_payday', datetoday)
	else: 		
		paydayamount=0
	return paydayamount

def paytaxes(bot, target):
	now = datetime.datetime.now()
	datetoday = int(now.strftime("%Y%j"))
	lasttaxday = bot.db.get_nick_value(target, 'spicebucks_taxday') or 0
	inbank = bot.db.get_nick_value(target, 'spicebucks_bank') or 0
	if lasttaxday == 0 or lasttaxday < datetoday:
		taxtotal = int(inbank * .1)
		spicebanktotal = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
		spicebucks(bot, 'SpiceBank', 'plus', taxtotal + spicebanktotal)
		spicebucks(bot, target, 'minus', taxtotal)
		bot.db.set_nick_value(target, 'spicebucks_taxday', datetoday)
		bot.say("Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicebucks will be transfered to the SpiceBot account.")
	else:
		bot.say("Taxes already paid today.")   

def transfer(bot, allusersinroomarray, instigator, target, amount):
	validamount = 0
	try:
		amount = int(amount)
		validamount = 1
	except:
		bot.say("I'm sorry, the amount you entered does not appear to be a number.")
		validamount = 0

	if validamount == 1:
		if amount <= 0:
			bot.say(instigator + " gave no spicefucks about " + target + "'s comment.")
		else:
			if target not in allusersinroomarray:
				bot.say("I'm sorry, I do not know who you want to transfer money to.")
			if target == instigator:
				bot.say("You cannot transfer spicebucks to yourself!")
			else:
				if spicebucks(bot, instigator, 'minus', amount) == 'true':
					spicebucks(bot, target, 'plus', amount)
					bot.say("You successfully transfered " + str(amount) + " spicebucks to " + target + ".") 

