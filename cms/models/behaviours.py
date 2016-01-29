from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.fields import RichTextField


class WithIntroduction(models.Model):
    intro = RichTextField(blank=True)

    class Meta:
        abstract = True
