from __future__ import unicode_literals

from django.db import models

from wagtail.core.fields import RichTextField, StreamField

from .streamfield import CMSStreamBlock


class WithFeedImage(models.Model):
    feed_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    class Meta:
        abstract = True


class WithIntroduction(models.Model):
    intro = RichTextField(blank=True)

    class Meta:
        abstract = True


class WithStreamField(models.Model):
    body = StreamField(CMSStreamBlock())

    class Meta:
        abstract = True
