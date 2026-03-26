import re
import unicodedata
from pathlib import Path

from django.core.management.base import BaseCommand

from movie.models import Movie


def normalize_title_for_filename(title):
    return re.sub(r'[<>:"/\\|?*]+', '', title).strip()


def ascii_normalize(value):
    normalized = unicodedata.normalize('NFKD', value)
    return normalized.encode('ascii', 'ignore').decode('ascii')


def canonicalize_filename_stem(value):
    value = ascii_normalize(value)
    value = value.lower()
    value = re.sub(r"[\"'`´]", "", value)
    value = re.sub(r"[:;,.!?]", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


class Command(BaseCommand):
    help = "Assign existing generated images from media/movie/images to each movie"

    def handle(self, *args, **kwargs):
        images_folder = Path(__file__).resolve().parents[3] / 'media' / 'movie' / 'images'
        if not images_folder.exists():
            self.stderr.write(f"Images folder not found: {images_folder}")
            return

        image_index = {}
        for image_path in images_folder.glob('*'):
            if image_path.is_file():
                image_index[canonicalize_filename_stem(image_path.stem)] = image_path.name

        updated_count = 0
        for movie in Movie.objects.all():
            filename = f"m_{normalize_title_for_filename(movie.title)}.png"
            image_path = images_folder / filename
            if not image_path.exists():
                canonical_title = canonicalize_filename_stem(f"m_{movie.title}")
                matched_name = image_index.get(canonical_title)
                if matched_name:
                    image_path = images_folder / matched_name
                else:
                    self.stderr.write(f"Image not found for {movie.title}: {filename}")
                    continue

            movie.image = f"movie/images/{image_path.name}"
            movie.save(update_fields=['image'])
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} images."))
