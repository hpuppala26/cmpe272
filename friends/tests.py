from django.test import TestCase,Client
from django.contrib.auth.models import User
from .forms import Searchu


class TestSearching(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser002@ts.com", password="Hello World")
        self.user2 = User.objects.create(username="testuser2", email="testuser2002@ts.com", password="Hello World")

    def test_searchbyusername(self):
        self.client = Client()
        self.client.force_login(self.user)
        response = self.client.post('/friends/matching/',
                                    {"search_namebyuser":"muk"})
        self.assertEqual(response.status_code, 200)

    def test_searchbyinterest(self):
        self.client = Client()
        self.client.force_login(self.user)
        response = self.client.post('/friends/matching/',
                                    {"search_namebyinterest":"networking,singing"})
        self.assertEqual(response.status_code, 200)

    def test_redirectingcase(self):
        self.client = Client()
        response = self.client.post('/friends/matching/',{"search_namebyuser":"muk"})
        self.assertEqual(response.status_code, 302)

    def test_sendingrequest(self):
        self.client = Client()
        self.client.force_login(self.user)
        response = self.client.post('/friends/sendr/',{"req":"testuser2"})
        self.assertEqual(response.status_code, 200)

    def test_acceptingingrequest(self):
        self.client = Client()
        self.client.force_login(self.user)
        sendresponse = self.client.post('/friends/sendr/',{"req":"testuser2"})
        # self.client.force_logout(self.user)
        self.client.force_login(self.user2)
        response = self.client.post('/friends/acceptr/',{"receiver":"testuser"})
        self.assertEqual(response.status_code, 200)

    def test_acceptingingrequest(self):
        self.client = Client()
        self.client.force_login(self.user)
        sendresponse = self.client.post('/friends/sendr/',{"req":"testuser2"})
        # self.client.force_logout(self.user)
        self.client.force_login(self.user2)
        response = self.client.post('/friends/decliner/',{"receiver":"testuser","option":'0'})
        self.assertEqual(response.status_code, 200)
# Create your tests here.
