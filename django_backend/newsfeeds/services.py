from newsfeeds.models import NewsFeed
from friendships.services import FriendshipServices

class NewsFeedServices(object):

    @classmethod
    def fanout_to_followers(cls, tweet):

        newsfeed = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipServices.get_followers(tweet.user)
        ]

        newsfeed.append(NewsFeed(user=tweet.user, tweet=tweet))
        NewsFeed.objects.bulk_create(newsfeed)
