from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel,
    StreamFieldPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index

from .carousel import AbstractCarouselItem
from .links import AbstractRelatedLink
from .streamfield import CMSStreamBlock


# HomePage
class HomePageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('HomePage', related_name='carousel_items')


class HomePageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('HomePage', related_name='related_links')


class HomePage(Page):
    body = StreamField(CMSStreamBlock())
    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    class Meta:
        verbose_name = 'Homepage'

HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
    InlinePanel('carousel_items', label='Carousel items'),
    InlinePanel('related_links', label='Related links'),
]

HomePage.promote_panels = Page.promote_panels


# IndexPage
class IndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('IndexPage', related_name='related_links')


class IndexPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

IndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel('related_links', label='Related links'),
]

IndexPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


# RichTextPage
class RichTextPageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('RichTextPage', related_name='carousel_items')


class RichTextPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('RichTextPage', related_name='related_links')


class RichTextPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

RichTextPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel('carousel_items', label='Carousel items'),
    FieldPanel('body', classname='full'),
    InlinePanel('related_links', label='Related links'),
]

RichTextPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
