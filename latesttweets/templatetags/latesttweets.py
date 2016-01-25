from django.conf import settings
from datetime import datetime
from django import template
from ..views import get_latesttweets
from twython import Twython


register = template.Library()

@register.inclusion_tag('latesttweets/tags/latesttweets.html',
                        takes_context=True)
def latesttweets(context):
    """Returns a cached list of recent tweets"""
    tweets = get_latesttweets(context['request'])

    return {'request': context['request'], 'tweets': tweets}


@register.filter()
def tweet_to_html(tweet):
    """Returns html for a curren tweet"""
    return Twython.html_for_tweet(tweet)


@register.assignment_tag(takes_context=False)
def get_twitter_user():
    """Current twitter user"""
    return settings.TWITTER_USER

@register.filter()
def parse_date_from_twitter(date_string):
    return datetime.strptime(date_string,'%a %b %d %H:%M:%S +0000 %Y')