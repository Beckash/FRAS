from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Contact


class ContactModelTest(TestCase):
    def setUp(self):
        Contact.objects.create(name='Abi')
        Contact.objects.create(email='abi@gmail.com')
        Contact.objects.create(message='just a test')

    def test_name_content(self):
        contact = Contact.objects.get(id=1)
        expected_object_name = f'{Contact.name}'
        self.assertEqual(expected_object_name, 'Abi')

    def test_email_content(self):
        contact = Contact.objects.get(id=1)
        expected_object_name = f'{Contact.email}'
        self.assertEqual(expected_object_name, 'abi@gmail.com')

    def test_message_content(self):
        contact = Contact.objects.get(id=1)
        expected_object_name = f'{Contact.message}'
        self.assertEqual(expected_object_name, 'just a test')


class HomePageViewTest(TestCase):
    def setUp(self):
        Contact.objects.create(text='this is another test')

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')
