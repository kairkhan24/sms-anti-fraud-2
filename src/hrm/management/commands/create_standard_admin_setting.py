from django.conf import settings
from django.core.management.base import BaseCommand

from hrm.models import AdminSettings


class Command(BaseCommand):

    def handle(self, *args, **options):
        if AdminSettings.objects.filter(name='Standard').first() is None:
            AdminSettings.objects.create(
                name='Standard',
                period_in_seconds=300,
                count_per_user=5
            )