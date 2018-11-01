# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.views.decorators.csrf import csrf_exempt
from .logger import *

def index(request):
    return render(request, 'chat/index.html', {})
@csrf_exempt
def room(request, room_name):

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'message_log':load_log(room_name)

    })
