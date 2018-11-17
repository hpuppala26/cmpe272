import os
from chat.models import Message
from django.db.models import Q
from .validator import *

def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

def log_message(sender,roomname,message):
    Message.objects.create(sender=sender,roomname=roomname,message=message)

def load_log(roomname):
    return Message.objects.filter(roomname=roomname)

def get_recents(username):
    messagelist=Message.objects.filter(Q(roomname__startswith=username)|Q(roomname__endswith=username)).order_by('-timestamp')
    recentlist = []
    for message in messagelist:
        if roomvalidate(username,message.roomname):
            recentlist.append(receiver_gen(username,message.roomname))
    return unique(recentlist)

def print_path():
    print(os.path.abspath(__file__))
