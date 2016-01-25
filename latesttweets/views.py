from django.conf import settings
from django.core.cache import cache
from twython import Twython, TwythonAuthError, TwythonError

import logging
logger = logging.getLogger(__name__)


def twitter_authenticate():
    """Authenticate to twitter"""

    try:
        twitter = Twython(settings.TWITTER_API_KEY,
                          settings.TWITTER_API_SECRET,
                          settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_TOKEN_SECRET)

    except TwythonAuthError as e:
        logger.warning(e)
        raise e

    return twitter


def get_latesttweets(request):

    tweets = cache.get('tweets')
    if tweets:
        return tweets

    try:
        t = twitter_authenticate()
        try:

            assert settings.TWITTER_LIST is not None

            tweets = t.get_list_statuses(
                slug=settings.TWITTER_LIST,
                owner_screen_name=settings.TWITTER_USER,
                count=settings.TWEETS_PER_PAGE)

        except (TwythonError, AssertionError):

            tweets = t.get_user_timeline(
                screen_name=settings.TWITTER_USER,
                count=settings.TWEETS_PER_PAGE)

    except TwythonAuthError as e:
        logger.info(e)
        return None

    cache.set('tweets', tweets, settings.TWITTER_TIMEOUT)

    return tweets
