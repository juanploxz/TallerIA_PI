from django.core.management.base import BaseCommand

from movie.models import Movie
from movie.recommendation_utils import cosine_similarity, get_embedding


class Command(BaseCommand):
    help = "Compare two movies and a prompt using embeddings"

    def handle(self, *args, **kwargs):
        movie1 = Movie.objects.filter(title__icontains="Schindler").first()
        movie2 = Movie.objects.filter(title__icontains="club").first()

        if not movie1 or not movie2:
            movies = list(Movie.objects.exclude(description='').order_by('id')[:2])
            if len(movies) < 2:
                self.stderr.write("Not enough movies with descriptions to compare.")
                return
            movie1, movie2 = movies

        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)
        prompt_emb = get_embedding("pelicula sobre la Segunda Guerra Mundial")

        self.stdout.write(
            f"Similaridad entre '{movie1.title}' y '{movie2.title}': {cosine_similarity(emb1, emb2):.4f}"
        )
        self.stdout.write(
            f"Similitud prompt vs '{movie1.title}': {cosine_similarity(prompt_emb, emb1):.4f}"
        )
        self.stdout.write(
            f"Similitud prompt vs '{movie2.title}': {cosine_similarity(prompt_emb, emb2):.4f}"
        )
