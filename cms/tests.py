import datetime

from cms.models.pages import (
    BlogIndexPage, BlogPost, EventIndexPage, EventPage, Gallery, HomePage,
    IndexPage, ReviewIndexPage, ReviewPage, RichTextPage, _paginate
)
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Site


class TestPages(TestCase):

    def test__paginate(self):
        items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

        factory = RequestFactory()

        request = factory.get('/test?page=1')
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                         _paginate(request, items).object_list)
        request = factory.get('/test?page=2')
        self.assertEqual([10, 11, 12, 13, 14, 15, 16, 17],
                         _paginate(request, items).object_list)
        request = factory.get('/test?page=10')
        self.assertEqual([10, 11, 12, 13, 14, 15, 16, 17],
                         _paginate(request, items).object_list)
        request = factory.get('/test?page=a')
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                         _paginate(request, items).object_list)


class TestHomePage(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(HomePage, {
            BlogIndexPage, EventIndexPage, IndexPage, ReviewIndexPage,
            RichTextPage, Gallery}
        )


class TestIndexPage(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(IndexPage, {IndexPage, RichTextPage})


class TestRichTextPage(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(RichTextPage, {})


class TestBlogIndexPage(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(BlogIndexPage, {BlogPost})

    def test_posts(self):
        bip = BlogIndexPage.objects.get(url_path='/home/blog/')

        self.assertEqual(2, bip.posts.count())
        self.assertEqual('post-2', bip.posts.first().slug)


class TestBlogPost(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(BlogPost, {})

    def test_blog_index(self):
        post = BlogPost.objects.first()
        expected = BlogIndexPage.objects.get(url_path='/home/blog/')

        self.assertEqual(expected, post.blog_index.specific)


class TestEventIndexPage(WagtailPageTests):
    fixtures = ['test.json']

    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get('/home/events/')
        self.request.site = Site.find_for_request(self.request)
        self.request.user = User.objects.create_user(username='test')

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(EventIndexPage, {EventPage})

    def test_past_events(self):
        # property
        eip = EventIndexPage.objects.get(url_path='/home/events/')

        past_events = eip.past_events
        self.assertEqual(2, past_events.count())
        self.assertEqual('event-1', past_events.first().slug)

        # view
        response = eip.get_past_events(self.request)
        self.assertEqual(200, response.status_code)

    def test_live_events(self):
        # property
        eip = EventIndexPage.objects.get(url_path='/home/events/')

        live_events = eip.live_events
        self.assertEqual(0, live_events.count())

        event = EventPage.objects.get(pk=12)
        event.date_from = datetime.date.today()
        event.save()

        live_events = eip.live_events
        self.assertEqual(1, live_events.count())

        event = EventPage.objects.get(pk=13)
        event.date_from = datetime.date.today()
        event.save()

        live_events = eip.live_events
        self.assertEqual(2, live_events.count())
        self.assertEqual('event-1', live_events.first().slug)

        # view
        response = eip.get_live_events(self.request)
        self.assertEqual(200, response.status_code)

    def test_pre_save_signal(self):
        event = EventPage.objects.get(pk=13)
        event.date_to = None

        self.assertIsNone(event.date_to)

        event.save()

        self.assertIsNotNone(event.date_to)
        self.assertEqual(event.date_from, event.date_to)


class TestEventPage(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(EventPage, {})

    def test_event_index(self):
        event = EventPage.objects.first()
        expected = EventIndexPage.objects.get(url_path='/home/events/')

        self.assertEqual(expected, event.event_index.specific)


class TestReviewIndexPage(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(ReviewIndexPage, {ReviewPage})

    def test_reviews(self):
        rip = ReviewIndexPage.objects.get(url_path='/home/reviews/')

        self.assertEqual(1, rip.reviews.count())
        self.assertEqual('my-first-review', rip.reviews.first().slug)


class TestReviewPage(WagtailPageTests):
    fixtures = ['test.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(ReviewPage, {})

    def test_review_index(self):
        review = ReviewPage.objects.first()
        expected = ReviewIndexPage.objects.get(url_path='/home/reviews/')

        self.assertEqual(expected, review.review_index.specific)
