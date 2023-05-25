from django.test import TestCase
from django.urls import reverse
from .models import ExampleModel

from .views import hello

class HelloTests(TestCase):
    def test_hello_view(self):
        url = reverse('hello')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'Hello, World!')

class DatabaseTests(TestCase):
    def test_model_creation(self):
        my_model = ExampleModel.objects.create(name='Name', description='description')
        self.assertEqual(my_model.name, 'Name')
        self.assertEqual(my_model.description, 'description')

    def test_model_query(self):
        ExampleModel.objects.create(name='Bob', description='the builder')

        models = ExampleModel.objects.all()
        self.assertEqual(models.count(), 1)
        self.assertEqual(models[0].name, 'Bob')
