from django.shortcuts import render
from .forms import Searchu,Searchi,SendRequest,ConfirmRequest
from .models import Confirmed_Friends,Pending_Requests
from accounts.models import UserProfile 
from django.contrib.auth.decorators import login_required
from collections import Counter
# Create your views here.


@login_required(login_url='/admin')
def sending_request(request):
    form = SendRequest()
    if request.method == "POST":
        form = SendRequest(request.POST)
        if form.is_valid():
            formdata=form.save(commit=False)
            formdata.sender=request.user.username
            formdata.save()
    return render(request, 'app/pending_request.html',{'form':form})

@login_required(login_url='/admin')
def accepting_request(request):
    form = ConfirmRequest()
    if request.method == "POST":
        form = ConfirmRequest(request.POST)
        if form.is_valid():
            acceptinglist=[]
            sendername=form.cleaned_data['Username2']
            acceptinglist.append(sendername)
            curruser=request.user.username
            acceptinglist.append(curruser)
            acceptinglist.sort()
            Confirmed_Friends.objects.create(Username1=acceptinglist[0],Username2=acceptinglist[1])
            Pending_Requests.objects.filter(sender=sendername,receiver=request.user.username).delete()
            #formdata=form.save(commit=False)
            #ormdata.username2=request.user.username



    return render(request, 'app/accept_request.html',{'form':form})



@login_required(login_url='/admin')
def friends_frndrequests(request):

    getfriends1=Confirmed_Friends.objects.filter(Username1=request.user.username)
    getfriends2=Confirmed_Friends.objects.filter(Username2=request.user.username)
    pendingfriends=Pending_Requests.objects.filter(receiver=request.user.username)

    pendingfrnd=[]
    friends=[]
    for frnd in getfriends1:
        friends.append(frnd.Username2)
    for frnd in getfriends2:
        friends.append(frnd.Username1)
    for frnds in pendingfriends:
        pendingfrnd.append(frnds.sender)
    friends=list(set(friends))
    pendingfrnd=list(set(pendingfrnd))
    return render(request, 'app/friends.html', {'friends':friends,'pendingfrnds':pendingfrnd})

@login_required(login_url='/admin')
def matching(request):
        form=Searchu(request.POST)
        form1=Searchi(request.POST)

        allusers=UserProfile.objects.all()
        getfriends1=Confirmed_Friends.objects.filter(Username1=request.user.username)
        getfriends2=Confirmed_Friends.objects.filter(Username2=request.user.username)
        friends=[]
        for frnd in getfriends1:
            friends.append(frnd.Username2)
        for frnd in getfriends2:
            friends.append(frnd.Username1)
        friends=list(set(friends))
        suggestionlist=[]
        #for suggestion finding current user city and interests
        for user in allusers:
            if str(user.user)==request.user.username:
                currusercity=user.city
                #currusercity=currusercity.lower()
                curruserinterest=str(user.interests)
                curruserinterest = curruserinterest.lower().replace(","," ").split(" ")
                curruserinterest = list(filter(None, curruserinterest))

        #otheruserlist = Interest_Model.objects.filter(interest__in=curruserinterest)
        #print(otheruserlist)
        for user in allusers:
            if str(user.user)!=request.user.username:
                otheruserinterest=str(user.interests)
                otheruserinterest = otheruserinterest.lower().replace(","," ").split(" ")
                otheruserinterest = list(filter(None, otheruserinterest))
                for item in curruserinterest:
                    if item in otheruserinterest:
                        suggestionlist.append(user.user)
            #suggestionlist.append(user.user)

        for user in allusers:
            if str(user.user)!=request.user.username:
                if str(user.city.lower()) == currusercity:
                    suggestionlist.append(user.user)

        # interestlist=Interest_Model.objects.filter(interest__in=text1)
        suggestionlist.sort(key=Counter(suggestionlist).get, reverse=True)
        suggestionlist = [ e
                        for i, e in enumerate(suggestionlist)
                          if suggestionlist.index(e) == i
                        ]
        suggestionlist= [x for x in suggestionlist if x.username not in friends]

        if form.is_valid():
            text=form.cleaned_data['search_namebyuser']
            userlist=UserProfile.objects.all()
            list2=[]
            for user in userlist:
                if str(user.user) == text and str(user.user) != str(request.user.username):
                    list2.append(user.user)
            return render(request, 'app/friendsugg.html', {'userlist':list2,'form':form,'form1':form1,'text':text,'suggestionlist':suggestionlist,'friends':friends})

        elif form1.is_valid():
            text1=form1.cleaned_data['search_namebyinterest']
            text1 = text1.lower().replace(","," ").split(" ")
            text1 = list(filter(None, text1))
            list1=[]

            for user in allusers:
                if str(user.user)!=request.user.username:
                    interestlist=str(user.interests)
                    #citylist=str(user.city)
                    interestlist = interestlist.lower().replace(","," ").split(" ")
                    interestlist = list(filter(None, interestlist))
                    if set(text1)==set(interestlist):
                        #print(interestlist)
                        list1.append(user.user)
            return render(request, 'app/friendsugg.html', {'interestlist':list1,'form':form,'form1':form1,'text1':text1,'currusercity':currusercity,'curruserinterest':curruserinterest,'suggestionlist':suggestionlist,'friends':friends})
        args = {'form':form,'form1':form1,'suggestionlist':suggestionlist,'friends':friends}
        return render(request, 'app/friendsugg.html', args)
