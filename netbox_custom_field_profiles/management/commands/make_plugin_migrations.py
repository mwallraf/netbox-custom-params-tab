from django.core.management.commands.makemigrations import Command as BaseCommand


class Command(BaseCommand):
    help = 'Generate migrations for netbox_custom_field_profiles (bypasses NetBox override)'

    def handle(self, *app_labels, **options):
        return super().handle('netbox_custom_field_profiles', **options)
