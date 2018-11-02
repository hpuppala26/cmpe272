# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from .logger import *
from .validator import *

@login_required(login_url='/admin/login/')
def index(request):
    return render(request, 'chat/index.html', {
        'userlist' : User.objects.all()
    })

@login_required(login_url='/admin/login/')
def room(request, room_name):
    if roomvalidate(request.user.username,room_name):
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'message_log':load_log(room_name)
            })
    else:
        return render(request,'chat/linkbroken.html',{})
