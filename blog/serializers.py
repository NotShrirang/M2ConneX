from rest_framework import serializers
from .models import Blog, BlogComment, BlogAction


class BlogSerializer(serializers.ModelSerializer):
    blogLikeCount = serializers.SerializerMethodField()
    blogDislikeCount = serializers.SerializerMethodField()
    blogReportCount = serializers.SerializerMethodField()
    blogCommentCount = serializers.SerializerMethodField()
    authorFirstName = serializers.SerializerMethodField()
    authorLastName = serializers.SerializerMethodField()
    authorEmail = serializers.SerializerMethodField()
    authorProfilePicture = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            'keywords',
            "image",
            "author",
            "authorFirstName",
            "authorLastName",
            "authorEmail",
            "authorProfilePicture",
            "blogLikeCount",
            "blogDislikeCount",
            "blogReportCount",
            "blogCommentCount",
            "isPublic",
            "isDrafted",
            "createdAt",
            "updatedAt",
        ]

    def get_blogLikeCount(self, obj):
        return obj.actions.filter(action="like").count()

    def get_blogDislikeCount(self, obj):
        return obj.actions.filter(action="dislike").count()

    def get_blogReportCount(self, obj):
        return obj.actions.filter(action="report").count()

    def get_blogCommentCount(self, obj):
        return obj.comments.count()

    def get_authorFirstName(self, obj):
        return obj.author.firstName

    def get_authorLastName(self, obj):
        return obj.author.lastName

    def get_authorEmail(self, obj):
        return obj.author.email

    def get_authorProfilePicture(self, obj):
        return obj.author.profilePicture


class BlogCommentSerializer(serializers.ModelSerializer):
    userFirstName = serializers.SerializerMethodField()
    userLastName = serializers.SerializerMethodField()
    userEmail = serializers.SerializerMethodField()
    userProfilePicture = serializers.SerializerMethodField()

    class Meta:
        model = BlogComment
        fields = [
            "id",
            "comment",
            "user",
            "userFirstName",
            "userLastName",
            "userEmail",
            "userProfilePicture",
            "createdAt",
            "updatedAt",
        ]

    def get_userFirstName(self, obj):
        return obj.user.firstName

    def get_userLastName(self, obj):
        return obj.user.lastName

    def get_userEmail(self, obj):
        return obj.user.email

    def get_userProfilePicture(self, obj):
        return obj.user.profilePicture


class BlogActionSerializer(serializers.ModelSerializer):
    userFirstName = serializers.SerializerMethodField()
    userLastName = serializers.SerializerMethodField()
    userEmail = serializers.SerializerMethodField()
    userProfilePicture = serializers.SerializerMethodField()

    class Meta:
        model = BlogAction
        fields = [
            "id",
            "action",
            "user",
            "userFirstName",
            "userLastName",
            "userEmail",
            "userProfilePicture",
            "createdAt",
            "updatedAt",
        ]

    def get_userFirstName(self, obj):
        return obj.user.firstName

    def get_userLastName(self, obj):
        return obj.user.lastName

    def get_userEmail(self, obj):
        return obj.user.email

    def get_userProfilePicture(self, obj):
        return obj.user.profilePicture
