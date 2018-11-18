from django.urls import path, include
from . import views

urlpatterns=[
    path('matching/',views.matching,name='matching'),
    path('send_request/',views.sending_request,name='sendrequest'),
    path('accept_request/',views.accepting_request,name='acceptrequest'),
    path('friends/',views.friends_frndrequests,name='friends_frndrequests'),
]
