import base64
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from movie.models import Movie
from movie.openai_utils import get_openai_client


def normalize_title_for_filename(title):
    return re.sub(r'[<>:"/\\|?*]+', '', title).strip()


class Command(BaseCommand):
    help = "Generate and save an image for the first movie using OpenAI"

    def handle(self, *args, **kwargs):
        client = get_openai_client()
        movie = Movie.objects.order_by('id').first()

        if not movie:
            self.stderr.write("No movies found in the database.")
            return

        images_folder = Path(__file__).resolve().parents[3] / 'media' / 'movie' / 'images'
        images_folder.mkdir(parents=True, exist_ok=True)

        response = client.images.generate(
            model="gpt-image-1",
            prompt=f"Movie poster of {movie.title}",
            size="1024x1024",
        )

        image_bytes = base64.b64decode(response.data[0].b64_json)

        filename = f"m_{normalize_title_for_filename(movie.title)}.png"
        full_path = images_folder / filename
        full_path.write_bytes(image_bytes)

        movie.image = f"movie/images/{filename}"
        movie.save(update_fields=['image'])
        self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))
