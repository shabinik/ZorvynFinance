import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Creates the initial admin user from environment variables"

    def handle(self, *args, **kwargs):
        email = os.getenv("ADMIN_EMAIL")
        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")

        if not all([email, username, password]):
            self.stdout.write("Skipping — ADMIN_EMAIL, ADMIN_USERNAME, ADMIN_PASSWORD not set.")
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"Admin {email} already exists. Skipping.")
            return

        User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
        )
        self.stdout.write(f"Admin user {email} created successfully.")