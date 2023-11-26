from django.urls import path, include, re_path
# from django.conf.urls import url
from . import views

urlpatterns=[
    
    path('matching/',views.matching,name='matching'),
    path('sendr/',views.sendr,name='sendr'),
    path('acceptr/',views.acceptr,name='acceptr'),
    path('decliner/',views.decliner,name='decliner'),
    path('accounts/profile/<str:username>', views.view_profile, name="profile"),
]
