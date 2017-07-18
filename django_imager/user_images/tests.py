from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from user_images.models import Photo, User
from faker import Faker
import factory
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    title = factory.Sequence(lambda n: "photo{}".format(n))
    image = SimpleUploadedFile(
        name='somephoto.jpg',

        path=open(os.path.join('media', 'title1.jpg'), 'rb').read(),

        content_type='image/jpeg'
    )


class HomePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='moocow', email='moocow@moo.com')
        self.user.save()


    def add_photos(self):

        photos = [PhotoFactory.build() for _ in range(10)]
        for photo in photos:
            photo.uploaded_by = self.user
            photo.save()

    def test_when_no_images_placeholder_appears(self):
        resp = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(resp.content, 'html.parser')
        self.assertTrue(html.find('img', {'src': "http://plaehold.ir/200x200"}))
