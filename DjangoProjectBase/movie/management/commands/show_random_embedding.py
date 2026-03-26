import numpy as np
from django.core.management.base import BaseCommand

from movie.models import Movie


class Command(BaseCommand):
    help = "Display the first values of a random stored movie embedding"

    def handle(self, *args, **kwargs):
        movie = Movie.objects.order_by('?').first()
        if not movie:
            self.stderr.write("No movies found in the database.")
            return

        vector = np.frombuffer(movie.emb, dtype=np.float32)
        self.stdout.write(f"{movie.title}: {vector[:10]}")
