from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from .links import AbstractLinkFields


class AbstractCarouselItem(AbstractLinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    embed_url = models.URLField('Embed URL', blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(AbstractLinkFields.panels, 'Link'),
    ]

    class Meta:
        abstract = True
