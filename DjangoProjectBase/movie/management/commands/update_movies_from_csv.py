import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from movie.models import Movie


class Command(BaseCommand):
    help = "Update movie descriptions in the database from the provided CSV"

    def handle(self, *args, **kwargs):
        csv_path = Path(__file__).resolve().parents[4] / 'aux_files' / 'updated_movie_descriptions.csv'
        if not csv_path.exists():
            self.stderr.write(f"CSV file not found: {csv_path}")
            return

        with csv_path.open(mode='r', encoding='utf-8', newline='') as file:
            rows = list(csv.DictReader(file))

        self.stdout.write(f"Found {len(rows)} movies in CSV")
        updated_count = 0

        for row in rows:
            title = row['Title']
            new_description = row['Updated Description']
            try:
                movie = Movie.objects.get(title=title)
                movie.description = new_description
                movie.save(update_fields=['description'])
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated: {title}"))
            except Movie.DoesNotExist:
                self.stderr.write(f"Movie not found: {title}")

        self.stdout.write(
            self.style.SUCCESS(f"Finished updating {updated_count} movies from CSV.")
        )
