
import os
import csv

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Models
from cride.circles.models import Circle


class Command(BaseCommand):
    def handle(self, *args, **options):
        file = os.path.join(settings.APPS_DIR, 'circles/management/commands/circles.csv')
        fields = []
        rows = []
        with open(file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)

        for row in rows:
            Circle.objects.get_or_create(
                name=row[0],
                slug_name=row[1],
                is_public=row[2],
                verified=row[3],
                members_limit=row[4],
            )