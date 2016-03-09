from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def load_event_categories(apps, schema_editor):
    """Creates the default event categories from the list provided in the
    settings."""
    EventCategory = apps.get_model('cms', 'EventCategory')

    for title in settings.EVENT_CATEGORIES:
        try:
            ev = EventCategory.objects.get(title=title)
        except ObjectDoesNotExist:
            ev = EventCategory(title=title)
            ev.save()


def unload_event_categories(apps, schema_editor):
    EventCategory = apps.get_model('cms', 'EventCategory')
    EventCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_homepage_announcement'),
    ]

    operations = [
        migrations.RunPython(load_event_categories,
                             reverse_code=unload_event_categories),
    ]
