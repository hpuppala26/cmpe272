from django import forms
from .models import Interest_Model,Pending_Requests,Confirmed_Friends
from django.contrib.auth.models import User


class registration_form(forms.ModelForm):


    class Meta:
        model=User
        fields=['username','first_name','last_name','email',]


class Forms_city(forms.ModelForm):

    class Meta:
        model=Interest_Model
        exclude = ['username',]

class Searchu(forms.Form):
    search_namebyuser = forms.CharField(max_length=100, required=True)
class Searchi(forms.Form):
    search_namebyinterest = forms.CharField(max_length=100, required=True)


class SendRequest(forms.ModelForm):

    class Meta:
        model=Pending_Requests
        fields = ['receiver',]




class ConfirmRequest(forms.ModelForm):
    #Username2=forms.CharField(label="friend requests:", widget=forms.Select(choices=requests))
    c_list = []
    pend_req = Pending_Requests.objects.filter()
    class Meta:
        model=Confirmed_Friends
        fields = ['Username2',]
