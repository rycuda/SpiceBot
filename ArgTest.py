import sopel.module

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    fullstring = trigger.group(2)
    triggerargsarray = create_args_array(fullstring)
    vr={}
    for num in range(1,4):
        vr[str(num)] = get_trigger_arg(triggerargsarray, num)
        bot.say(str(vr["3"]))
        

def create_args_array(fullstring):
    triggerargsarray = []
    for word in fullstring.split():
        triggerargsarray.append(word)
    return triggerargsarray

def get_trigger_arg(triggerargsarray, number):
    number = number - 1
    try:
        triggerarg = triggerargsarray[number]
    except IndexError:
        triggerarg = ''
    return triggerarg


