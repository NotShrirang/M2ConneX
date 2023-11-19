from .models import (
    Feed,
    FeedImage,
    FeedAction,
    FeedActionComment
)

from CODE.filters import CODEDateFilter


class FeedFilter(CODEDateFilter):
    class Meta:
        model = Feed
        fields = {
            'subject': ['exact', 'icontains'],
            'body': ['exact', 'icontains'],
            'user': ['exact'],
        }


class FeedImageFilter(CODEDateFilter):
    class Meta:
        model = FeedImage
        fields = {
            'feed': ['exact'],
            'coverImage': ['exact'],
        }


class FeedActionFilter(CODEDateFilter):
    class Meta:
        model = FeedAction
        fields = {
            'feed': ['exact'],
            'action': ['exact'],
            'user': ['exact'],
        }


class FeedActionCommentFilter(CODEDateFilter):
    class Meta:
        model = FeedActionComment
        fields = {
            'feedAction__feed': ['exact'],
            'comment': ['exact', 'icontains'],
            'feedAction__user': ['exact'],
        }
