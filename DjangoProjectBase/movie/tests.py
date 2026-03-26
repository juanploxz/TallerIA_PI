from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Movie


class MovieViewsTests(TestCase):
    def setUp(self):
        Movie.objects.create(
            title='La lista de Schindler',
            description='Drama historico ambientado en la Segunda Guerra Mundial.',
            genre='Drama',
            year=1993,
        )
        Movie.objects.create(
            title='El club de la pelea',
            description='Drama psicologico sobre identidad y violencia.',
            genre='Drama',
            year=1999,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_statistics_page_loads(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)

    def test_update_movies_from_csv_command_updates_descriptions(self):
        call_command('update_movies_from_csv', stdout=StringIO(), stderr=StringIO())
        self.assertTrue(
            Movie.objects.exclude(description='').filter(title='La lista de Schindler').exists()
        )

    def test_update_images_from_folder_does_not_crash(self):
        images_folder = Path(__file__).resolve().parents[1] / 'media' / 'movie' / 'images'
        images_folder.mkdir(parents=True, exist_ok=True)
        for movie in Movie.objects.all():
            (images_folder / f"m_{movie.title}.png").write_bytes(b'test')

        call_command('update_images_from_folder', stdout=StringIO(), stderr=StringIO())
        self.assertTrue(
            Movie.objects.filter(title='La lista de Schindler', image__icontains='m_').exists()
        )

    @patch('movie.recommendation_utils.get_embedding')
    def test_find_best_movie_page_renders_result(self, mock_get_embedding):
        import numpy as np

        mock_get_embedding.return_value = np.ones(1536, dtype=np.float32)
        for movie in Movie.objects.all():
            movie.emb = np.ones(1536, dtype=np.float32).tobytes()
            movie.save(update_fields=['emb'])

        response = self.client.get(reverse('recommendations:search'), {'prompt': 'drama'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'La lista de Schindler')
