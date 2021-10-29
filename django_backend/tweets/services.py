from tweets.models import TweetPhoto


class TweetService(object):

    @classmethod
    def create_photos_from_files_for_tweet(cls, tweet, files):
        photos = []
        for index, file in enumerate(files):
            photo = TweetPhoto(
                tweet=tweet,
                user=tweet.user,
                file=file,
                order=index,
            )
            photos.append(photo)
        TweetPhoto.objects.bulk_create(photos)
