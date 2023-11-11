from feed.models import Feed, FeedImage, FeedAction, FeedActionComment
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class FeedSerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()

    class Meta:
        model = Feed
        fields = ['id', 'subject', 'body', 'user', 'createdAt', 'updatedAt', 'userName', 'profilePicture']
        list_fields = ['id', 'subject', 'body', 'user', 'createdAt', 'updatedAt', 'userName', 'profilePicture']
        get_fields = ['id', 'subject', 'body', 'user', 'createdAt', 'updatedAt', 'userName', 'profilePicture']

    def get_userName(self, obj):
        return (obj.user.firstName or "") + " " + (obj.user.lastName or "")

    def get_profilePicture(self, obj):
        return obj.user.profilePicture or ""


class FeedImageSerializer(ModelSerializer):
    feedName = SerializerMethodField()

    class Meta:
        model = FeedImage
        fields = ['id', 'image', 'coverImage', 'createdAt', 'updatedAt', 'feedName']
        list_fields = ['id', 'image', 'coverImage', 'createdAt', 'updatedAt', 'feedName']
        get_fields = ['id', 'image', 'coverImage', 'createdAt', 'updatedAt', 'feedName']

    def get_feedName(self, obj):
        return obj.feed.subject


class FeedActionSerializer(ModelSerializer):
    feedName = SerializerMethodField()
    userName = SerializerMethodField()

    class Meta:
        model = FeedAction
        fields = ['id', 'feed', 'action', 'user', 'createdAt', 'updatedAt', 'feedName', 'userName']
        list_fields = ['id', 'feed', 'action', 'user', 'createdAt', 'updatedAt', 'feedName', 'userName']
        get_fields = ['id', 'feed', 'action', 'user', 'createdAt', 'updatedAt', 'feedName', 'userName']

    def get_feedName(self, obj):
        return obj.feed.subject

    def get_userName(self, obj):
        return (obj.user.firstName or "") + " " + (obj.user.lastName or "")


class FeedActionCommentSerializer(ModelSerializer):
    feedName = SerializerMethodField()
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()

    class Meta:
        model = FeedActionComment
        fields = ['id', 'feed_action', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']
        list_fields = ['id', 'feed_action', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']
        get_fields = ['id', 'feed_action', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']

    def get_feedName(self, obj):
        return obj.feed_action.feed.subject

    def get_userName(self, obj):
        return (obj.feed_action.user.firstName or "") + " " + (obj.feed_action.user.lastName or "")

    def get_profilePicture(self, obj):
        return obj.feed_action.user.profilePicture or ""
