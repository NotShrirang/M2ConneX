from feed.models import Feed, FeedImage, FeedAction, FeedActionComment
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class FeedSerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()
    likesCount = SerializerMethodField()
    commentsCount = SerializerMethodField()
    sharesCount = SerializerMethodField()

    class Meta:
        model = Feed
        fields = ['id', 'subject', 'body', 'user', 'createdAt', 'updatedAt', 'userName', 'profilePicture', 'likesCount', 'commentsCount', 'sharesCount']
        list_fields = fields
        get_fields = fields

    def get_userName(self, obj):
        return (obj.user.firstName or "") + " " + (obj.user.lastName or "")

    def get_profilePicture(self, obj):
        return obj.user.profilePicture or ""
    
    def get_likesCount(self, obj):
        return obj.actions.filter(action='LIKE').count()
    
    def get_commentsCount(self, obj):
        return obj.actions.filter(action='COMMENT').count()
    
    def get_sharesCount(self, obj):
        return obj.actions.filter(action='SHARE').count()


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
        fields = ['id', 'feedAction', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']
        list_fields = ['id', 'feedAction', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']
        get_fields = ['id', 'feedAction', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']

    def get_feedName(self, obj):
        return obj.feedAction.feed.subject

    def get_userName(self, obj):
        return (obj.feedAction.user.firstName or "") + " " + (obj.feedAction.user.lastName or "")

    def get_profilePicture(self, obj):
        return obj.feedAction.user.profilePicture or ""
