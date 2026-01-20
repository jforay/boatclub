from django.core.management.base import BaseCommand
from django.utils.text import slugify
from boats_and_locations.models import Boat

class Command(BaseCommand):
    help = "Backfill slug field for existing Boat records"

    def handle(self, *args, **options):
        updated = 0

        for boat in Boat.objects.all():
            if boat.slug:
                continue

            base = slugify(boat.name)
            slug = base
            i = 2
            while Boat.objects.filter(slug=slug).exclude(pk=boat.pk).exists():
                slug = f"{base}-{i}"
                i += 1

            boat.slug = slug
            boat.save(update_fields=["slug"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Backfilled {updated} boat slugs."))
