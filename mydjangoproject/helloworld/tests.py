from django.test import TestCase

from __future__ import annotations

from django.test import TestCase
from django.urls import reverse
from .models import City
# from .views import hello


class HelloViewTests(TestCase):
    def test_index_view(self: HelloViewTests) -> None:
        response = self.client.get("/")
        assert response.status_code == 200
   
class HelloTests(TestCase):
    def test_hello_view(self):
        url = reverse('hello')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'Hello, World!')

class DatabaseTests(TestCase):
    def test_model_creation(self):
        my_model = City.objects.create(city='citya', description='description')
        self.assertEqual(my_model.city, 'citya')
        self.assertEqual(my_model.description, 'description')

    def test_model_query(self):
        City.objects.create(city='Bob', description='the builder')

        models = City.objects.all()
        self.assertEqual(models.count(), 1)
        self.assertEqual(models[0].city, 'Bob')

