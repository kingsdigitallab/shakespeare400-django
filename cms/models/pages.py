from __future__ import unicode_literals

from datetime import date

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from .behaviours import WithFeedImage, WithIntroduction, WithStreamField
from .carousel import AbstractCarouselItem
from .links import AbstractRelatedLink

import logging

logger = logging.getLogger(__name__)


# HomePage
class HomePageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('HomePage', related_name='carousel_items')


class HomePageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('HomePage', related_name='related_links')


class HomePage(Page, WithStreamField):
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


class IndexPage(Page, WithFeedImage, WithIntroduction):
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


class RichTextPage(Page, WithFeedImage):
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

RichTextPage.content_panels = [
    FieldPanel('title', classname='full title'),
    InlinePanel('carousel_items', label='Carousel items'),
    FieldPanel('body', classname='full'),
    InlinePanel('related_links', label='Related links'),
]

RichTextPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


def _paginate(request, items):
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    try:
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        items = paginator.page(1)

    return items


# Blogs
# BlogIndexPage
class BlogIndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('BlogIndexPage', related_name='related_links')


class BlogIndexPage(RoutablePageMixin, Page, WithIntroduction):
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        # gets list of live blog posts that are descendants of this page
        posts = BlogPost.objects.live().descendant_of(self)

        # orders by most recent date first
        posts = posts.order_by('-date')

        return posts

    @route(r'^$')
    def all_posts(self, request):
        posts = self.posts
        logger.debug('Posts: {}'.format(posts))

        return render(request, self.get_template(request),
                      {'self': self, 'posts': _paginate(request, posts)})

    @route(r'^author/(?P<author>[\w ]+)/$')
    def author(self, request, author=None):
        if not author:
            # Invalid author filter
            logger.error('Invalid author filter')
            return self.all_posts(request)

        posts = self.posts.filter(owner__username=author)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'author', 'filter': author
            }
        )

    @route(r'^tag/(?P<tag>[\w ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': self._paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )

BlogIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel('related_links', label='Related links'),
]

BlogIndexPage.promote_panels = Page.promote_panels


# BlogPost
class BlogPostCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('BlogPost', related_name='carousel_items')


class BlogPostRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('BlogPost', related_name='related_links')


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items')


class BlogPost(Page, WithFeedImage, WithStreamField):
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    date = models.DateField('Post date')

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    subpage_types = ['BlogPost']

    @property
    def blog_index(self):
        # finds closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

BlogPost.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    StreamFieldPanel('body'),
    InlinePanel('carousel_items', label='Carousel items'),
    InlinePanel('related_links', label='Related links'),
]

BlogPost.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]


# Events
# EventIndexPage
class EventIndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('EventIndexPage', related_name='related_links')


class EventIndexPage(Page, RoutablePageMixin, WithIntroduction):
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    @property
    def events(self):
        # gets list of live event pages that are descendants of this page
        events = EventPage.objects.live().descendant_of(self)

        # filters events list to get ones that are either
        # running now or start in the future
        events = events.filter(date_from__gte=date.today())

        # orders by date
        events = events.order_by('date_from')

        return events

EventIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel('related_links', label='Related links'),
]

EventIndexPage.promote_panels = Page.promote_panels


# EventPage
class EventCategory(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Event categories'

register_snippet(EventCategory)


class EventPageCategory(Orderable):
    page = ParentalKey('EventPage', related_name='categories')

    category = models.ForeignKey(EventCategory)

    panels = [
        SnippetChooserPanel('category')
    ]


class EventPageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('EventPage', related_name='carousel_items')


class EventPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('EventPage', related_name='related_links')


class EventPage(Page, WithFeedImage, WithStreamField):
    date_from = models.DateField('Start date')
    date_to = models.DateField(
        'End date', null=True, blank=True,
        help_text='Not required if event is on a single day'
    )
    time_from = models.TimeField('Start time', null=True, blank=True)
    time_to = models.TimeField('End time', null=True, blank=True)
    location = models.CharField(max_length=256)
    signup_link = models.URLField(null=True, blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('location'),
        index.SearchField('body'),
    )

    @property
    def event_index(self):
        # finds closest ancestor which is an event index
        return self.get_ancestors().type(EventIndexPage).last()

EventPage.content_panels = [
    FieldPanel('title', classname='full title'),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('date_from', classname='col6'),
            FieldPanel('date_to', classname='col6'),
        ], classname='full'),
        FieldRowPanel([
            FieldPanel('time_from', classname='col6'),
            FieldPanel('time_to', classname='col6'),
        ], classname='full'),
    ], 'Dates'),
    FieldPanel('location'),
    InlinePanel('categories', label='Categories'),
    InlinePanel('carousel_items', label='Carousel items'),
    FieldPanel('body', classname='full'),
    FieldPanel('signup_link'),
    InlinePanel('related_links', label='Related links'),
]

EventPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


# Reviews
# ReviewIndexPage
class ReviewIndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('ReviewIndexPage', related_name='related_links')


class ReviewIndexPage(Page, RoutablePageMixin, WithIntroduction):
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    @property
    def reviews(self):
        # gets list of live review pages that are descendants of this page
        reviews = ReviewPage.objects.live().descendant_of(self)

        # orders by most recent date first
        reviews = reviews.order_by('-date')

        return reviews

ReviewIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel('related_links', label='Related links'),
]

ReviewIndexPage.promote_panels = Page.promote_panels


# ReviewPage
class ReviewPageCategory(Orderable):
    page = ParentalKey('ReviewPage', related_name='categories')

    category = models.ForeignKey(EventCategory)

    panels = [
        SnippetChooserPanel('category')
    ]


class ReviewPageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('ReviewPage', related_name='carousel_items')


class ReviewPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('ReviewPage', related_name='related_links')


class ReviewPage(Page, WithFeedImage, WithStreamField):
    date = models.DateField('Post date')

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    @property
    def review_index(self):
        # finds closest ancestor which is a review index
        return self.get_ancestors().type(ReviewIndexPage).last()

ReviewPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    InlinePanel('categories', label='Categories'),
    StreamFieldPanel('body'),
    InlinePanel('carousel_items', label='Carousel items'),
    InlinePanel('related_links', label='Related links'),
]

ReviewPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]
