from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from bs4 import BeautifulSoup


class RegistrationTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_registration_page_uses_proper_template(self):
        response = self.client.get(reverse('registration_register'))
        self.assertIn('registration/registration_form.html', response.template_name)

    def test_upon_registration_a_new_user_is_created(self):
        self.assertTrue(User.objects.count() == 0)
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content)

        token = html.find('input', {'name': 'csfrmiddlewaretoken'}).attrs['value']

        data_dict = {
            'csfrmiddlewaretoken': token,
            'username': 'bob',
            'email': 'bob@bob.com',
            'password1': 'iambob_thebobbiest',
            'password2': 'iambob_thebobbiest',
        }
        self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertTrue(User.objects.count() == 1)

    def test_upon_registration_an_email_is_sent(self):
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content)

        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']
        self.assertTrue(len(mail.outbox) == 0)
        data_dict = {
            'csfrmiddlewaretoken': token,
            'username': 'bob',
            'email': 'bob@bob.com',
            'password1': 'iambob_thebobbiest',
            'password2': 'iambob_thebobbiest',
        }
        self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertTrue(User.objects.count() == 1)