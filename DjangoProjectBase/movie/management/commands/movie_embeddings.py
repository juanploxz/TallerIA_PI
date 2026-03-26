from django.core.management.base import BaseCommand

from movie.models import Movie
from movie.recommendation_utils import get_embedding


class Command(BaseCommand):
    help = "Generate and store embeddings for all movies in the database"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            if not movie.description:
                self.stderr.write(f"Skipping {movie.title}: empty description")
                continue

            embedding = get_embedding(movie.description)
            movie.emb = embedding.tobytes()
            movie.save(update_fields=['emb'])
            self.stdout.write(self.style.SUCCESS(f"Embedding stored for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS("Finished generating embeddings for all movies"))
