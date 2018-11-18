from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#class UserProfile_Model(models.Model):
#    username=models.OneToOneField(User,on_delete=models.CASCADE);
#    city = models.CharField(max_length=100,null=True);
#    phone = models.IntegerField(default=10);


#    def __str__(self):
#            return str(self.username)


class Interest_Model(models.Model):
    interestid = models.AutoField(primary_key=True)
    username=models.OneToOneField(User,on_delete=models.CASCADE);
    interest = models.CharField(max_length=100,default='');
    city = models.CharField(max_length=200)

    def __str__(self):
            return str(self.username)

class Pending_Requests(models.Model):
    sender = models.CharField(max_length=100,default='')
    receiver = models.CharField(max_length=100)

    def __str__(self):
        return str(self.receiver)

class Confirmed_Friends(models.Model):
    Username1 = models.CharField(max_length=100)
    Username2 = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Username2)
