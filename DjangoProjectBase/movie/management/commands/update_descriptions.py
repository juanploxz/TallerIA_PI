from django.core.management.base import BaseCommand

from movie.models import Movie
from movie.openai_utils import get_openai_client


class Command(BaseCommand):
    help = "Update the description of the first movie using OpenAI"

    def handle(self, *args, **kwargs):
        client = get_openai_client()
        movie = Movie.objects.order_by('id').first()

        if not movie:
            self.stderr.write("No movies found in the database.")
            return

        prompt = (
            "Vas a actuar como un aficionado del cine que sabe describir de forma clara, "
            "concisa y precisa cualquier pelicula en menos de 200 palabras. "
            "La descripcion debe incluir el genero de la pelicula y cualquier informacion "
            "adicional que sirva para crear un sistema de recomendacion. "
            f"Actualiza la descripcion '{movie.description}' de la pelicula '{movie.title}'."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        movie.description = response.choices[0].message.content.strip()
        movie.save(update_fields=['description'])
        self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))
