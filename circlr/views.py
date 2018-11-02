from django.shortcuts import render,HttpResponse
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return HttpResponse("Loggged out<br> <a href='/chat'>chat</a>")
