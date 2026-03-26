from django.test import TestCase
from django.urls import reverse

from movie.models import Movie


class RecommendationViewTests(TestCase):
    def test_page_loads_without_prompt(self):
        response = self.client.get(reverse('recommendations:search'))
        self.assertEqual(response.status_code, 200)

    def test_page_handles_missing_api_key_gracefully(self):
        Movie.objects.create(title='Test Movie', description='Test description')
        response = self.client.get(reverse('recommendations:search'), {'prompt': 'war movie'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OpenAI API key not found')
