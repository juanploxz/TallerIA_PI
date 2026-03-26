import re
from pathlib import Path

from django.core.management.base import BaseCommand

from movie.models import Movie


def normalize_title_for_filename(title):
    return re.sub(r'[<>:"/\\|?*]+', '', title).strip()


class Command(BaseCommand):
    help = "Assign existing generated images from media/movie/images to each movie"

    def handle(self, *args, **kwargs):
        images_folder = Path(__file__).resolve().parents[3] / 'media' / 'movie' / 'images'
        if not images_folder.exists():
            self.stderr.write(f"Images folder not found: {images_folder}")
            return

        updated_count = 0
        for movie in Movie.objects.all():
            filename = f"m_{normalize_title_for_filename(movie.title)}.png"
            image_path = images_folder / filename
            if not image_path.exists():
                self.stderr.write(f"Image not found for {movie.title}: {filename}")
                continue

            movie.image = f"movie/images/{filename}"
            movie.save(update_fields=['image'])
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} images."))
