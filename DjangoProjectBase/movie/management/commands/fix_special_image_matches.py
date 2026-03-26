from pathlib import Path

from django.core.management.base import BaseCommand

from movie.models import Movie


SPECIAL_IMAGE_MATCHES = {
    "Fairyland: A Kingdom of Fairies": [
        "m_Fairyland A Kingdom of Fairies.png",
        "m_Fairyland_ A Kingdom of Fairies.png",
        "m_Fairyland.png",
    ],
    "The '?' Motorist": [
        "m_The Motorist.png",
        "m_The '?' Motorist.png",
        "m_The '' Motorist.png",
    ],
    "The Avenging Conscience: or 'Thou Shalt Not Kill'": [
        "m_The Avenging Conscience or Thou Shalt Not Kill.png",
        "m_The Avenging Conscience or 'Thou Shalt Not Kill'.png",
        "m_The Avenging Conscience.png",
    ],
    "The India Rubber Head": [
        "m_The India Rubber Head.png",
    ],
    "The Inside of the White Slave Traffic": [
        "m_The Inside of the White Slave Traffic.png",
    ],
}


class Command(BaseCommand):
    help = "Assign images for movie titles with special filename cases"

    def handle(self, *args, **kwargs):
        images_folder = Path(__file__).resolve().parents[3] / 'media' / 'movie' / 'images'
        if not images_folder.exists():
            self.stderr.write(f"Images folder not found: {images_folder}")
            return

        updated_count = 0
        for title, candidate_filenames in SPECIAL_IMAGE_MATCHES.items():
            movie = Movie.objects.filter(title=title).first()
            if not movie:
                self.stderr.write(f"Movie not found: {title}")
                continue

            matched_file = None
            for filename in candidate_filenames:
                candidate_path = images_folder / filename
                if candidate_path.exists():
                    matched_file = filename
                    break

            if not matched_file:
                self.stderr.write(f"Image not found for {title}")
                continue

            movie.image = f"movie/images/{matched_file}"
            movie.save(update_fields=['image'])
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updated image for: {title}"))

        self.stdout.write(
            self.style.SUCCESS(f"Finished updating {updated_count} special-case images.")
        )
