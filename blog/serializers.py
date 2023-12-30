from rest_framework import serializers
from .models import Blog, BlogComment, BlogAction


class BlogSerializer(serializers.ModelSerializer):
    authorFirstName = serializers.SerializerMethodField()
    authorLastName = serializers.SerializerMethodField()
    authorEmail = serializers.SerializerMethodField()
    authorProfilePicture = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()

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
            "isPublic",
            "isDrafted",
            "likes",
            "comments",
            "isLiked",
            "createdAt",
            "updatedAt",
        ]

    def get_authorFirstName(self, obj):
        return obj.author.firstName

    def get_authorLastName(self, obj):
        return obj.author.lastName

    def get_authorEmail(self, obj):
        return obj.author.email

    def get_authorProfilePicture(self, obj):
        return obj.author.profilePicture

    def get_likes(self, obj):
        likes = BlogAction.objects.filter(action="like", blog=obj)
        return BlogActionSerializer(likes, many=True).data

    def get_comments(self, obj):
        comments = BlogComment.objects.filter(
            action__blog=obj).order_by('-createdAt')
        return BlogCommentSerializer(comments, many=True).data

    def get_isLiked(self, obj):
        try:
            BlogAction.objects.get(
                action="like", blog=obj, user=self.context['request'].user)
            return True
        except BlogAction.DoesNotExist:
            return False


class BlogActionSerializer(serializers.ModelSerializer):
    userFirstName = serializers.SerializerMethodField()
    userLastName = serializers.SerializerMethodField()
    userEmail = serializers.SerializerMethodField()
    userProfilePicture = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = BlogAction
        fields = [
            "id",
            "blog",
            "action",
            "user",
            "userFirstName",
            "userLastName",
            "userEmail",
            "userProfilePicture",
            "comment",
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

    def get_comment(self, obj):
        try:
            return obj.comments.first().comment
        except AttributeError:
            return None


class BlogCommentSerializer(serializers.ModelSerializer):
    userFirstName = serializers.SerializerMethodField()
    userLastName = serializers.SerializerMethodField()
    userEmail = serializers.SerializerMethodField()
    userProfilePicture = serializers.SerializerMethodField()

    class Meta:
        model = BlogComment
        fields = [
            "id",
            "action",
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
