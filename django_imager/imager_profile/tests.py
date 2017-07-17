from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from user_images.models import Photo, User
from faker import Faker
import factory
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# class PhotoFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Photo

#     title = factory.Sequence(lambda n: "photo{}".format(n))
#     image = SimpleUploadedFile(
#         name='somephoto.jpg',
#         path=open(os.path.join(BASE_DIR, 'MEDIA', 'photos', 'somephoto.jpg'), 'rb').read()
#         content_type='image/jpeg'
#     )


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

    # def test_when_user_logins_redirect_to_home_page(self):
    #     resp = self.client.post(reverse_lazy('login'), {
    #             'username': self.user.username, 'password': 'moomoomoo'
    #     })
    #     self.assertTrue(resp.url == reverse_lazy('imager_profile:profile'))
