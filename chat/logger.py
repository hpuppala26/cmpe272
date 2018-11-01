import os
from chat.models import Message
def log_message(sender,roomname,message):
    Message.objects.create(sender=sender,roomname=roomname,message=message)

def load_log(roomname):
    return Message.objects.filter(roomname=roomname)
def print_path():
    print(os.path.abspath(__file__))
