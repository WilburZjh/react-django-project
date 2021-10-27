from notifications.signals import notify
from tweets.models import Tweet
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType


class NotificationService(object):

    @classmethod
    def send_like_notification(cls, like):
        target = like.content_object

        if like.user == target.user:
            return

        if like.content_type == ContentType.objects.get_for_model(Tweet):
            notify.send(
                like.user,
                verb='liked your tweet.',
                recipient=target.user,
                target=target,
            )
        if like.content_type == ContentType.objects.get_for_model(Comment):
            notify.send(
                like.user,
                verb='liked your comment.',
                recipient=target.user,
                target=target,
            )


    @classmethod
    def send_comment_notification(cls, comment):
        if comment.user == comment.tweet.user:
            return
        notify.send(
            comment.user,
            verb='commented on your Tweet.',
            recipient=comment.tweet.user,
            target=comment.tweet,
        )
