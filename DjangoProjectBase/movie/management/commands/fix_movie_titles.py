from django.core.management.base import BaseCommand

from movie.models import Movie


TITLE_FIXES = {
    "Employees Leaving the Lumi\ufffdre Factory": "Employees Leaving the Lumière Factory",
    "D\ufffdmolition d'un mur": "Démolition d'un mur",
    "Faust et M\ufffdphistoph\ufffdl\ufffds": "Faust et Méphistophélès",
    "Tr\ufffddg\ufffdrdsm\ufffdstaren": "Trädgårdsmästaren",
}


class Command(BaseCommand):
    help = "Fix known movie titles with broken character encoding"

    def handle(self, *args, **kwargs):
        updated_count = 0

        for broken_title, fixed_title in TITLE_FIXES.items():
            movie = Movie.objects.filter(title=broken_title).first()
            if not movie:
                self.stdout.write(f"Not found: {broken_title}")
                continue

            movie.title = fixed_title
            movie.save(update_fields=['title'])
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updated: {fixed_title}"))

        self.stdout.write(
            self.style.SUCCESS(f"Finished fixing {updated_count} movie titles.")
        )
