from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from movie.models import Movie


class RecommendationViewTests(TestCase):
    def test_page_loads_without_prompt(self):
        response = self.client.get(reverse('recommendations:search'))
        self.assertEqual(response.status_code, 200)

    @patch('recommendations.views.find_best_movie_for_prompt')
    def test_page_handles_recommendation_errors_gracefully(self, mock_find_best_movie_for_prompt):
        mock_find_best_movie_for_prompt.side_effect = RuntimeError('OpenAI API key not found')
        response = self.client.get(reverse('recommendations:search'), {'prompt': 'war movie'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OpenAI API key not found')

    @patch('recommendations.views.find_best_movie_for_prompt')
    def test_page_shows_recommended_movie_result(self, mock_find_best_movie_for_prompt):
        movie = Movie.objects.create(
            title='War Epic',
            description='A historical war drama.',
            genre='Drama',
            year=1915,
        )
        mock_find_best_movie_for_prompt.return_value = (movie, 0.9876)

        response = self.client.get(
            reverse('recommendations:search'),
            {'prompt': 'pelicula de guerra'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recommendation for: pelicula de guerra')
        self.assertContains(response, 'War Epic')
        self.assertContains(response, 'A historical war drama.')
        self.assertContains(response, 'Similarity: 0.9876')
