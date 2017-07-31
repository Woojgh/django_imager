from django.test import TestCase, Client
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from user_images.models import User
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class ProfilePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='moocow', email='moocow@moo.com')
        self.user.save()

    def test_users_profile_info_on_profile_page(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('profile'))
        html = BeautifulSoup(resp.content, "html.parser")
        self.assertTrue(self.user.username.encode('utf8') in resp.content)
        self.assertTrue(b'<li>Email:</li>' not in html)

        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('profile'))
        self.assertTrue(bytes(reverse_lazy('library').encode('utf8')) not in resp.content)
