"""Management command for exporting application data."""

from django.contrib.auth.models import User
from django.core import serializers
from django.core.management.base import BaseCommand

from lettings.models import Address, Letting
from profiles.models import Profile


class Command(BaseCommand):
    """Export application data to a Django fixture."""

    help = "Export application data, excluding superusers."

    def handle(self, *args, **options):
        """Export users, profiles, addresses, and lettings."""
        users = User.objects.filter(is_superuser=False)

        objects = [
            *users,
            *Profile.objects.filter(user__is_superuser=False),
            *Address.objects.all(),
            *Letting.objects.all(),
        ]

        data = serializers.serialize("json", objects, indent=2)

        with open("data.json", "w", encoding="utf-8") as fixture:
            fixture.write(data)

        self.stdout.write(self.style.SUCCESS("Data exported successfully to data.json."))
