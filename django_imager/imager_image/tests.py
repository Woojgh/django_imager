from django.test import Client, RequestFactory, TestCase

# Create your tests here.


class ProfileVieTests(TestCase):

    def setUo(self):
        self.client = Client()
        self.req_factory = RequestFactory()
        