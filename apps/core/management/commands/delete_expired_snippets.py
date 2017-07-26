
from django.core.management import BaseCommand
from django.utils import timezone

from apps.snippet.models import Snippet


class Command(BaseCommand):

    def handle(self, **options):
        now = timezone.now()
        expired_snippets, _ = Snippet.objects.filter(expiry_date__lte=now).delete()
        self.stdout.write(f"Deleting expired snippets. Total objects deleted: {expired_snippets}")

