from feed.models import (
    Feed,
    FeedImage,
    FeedAction,
    FeedActionComment
)
from feed.serializers import (
    FeedSerializer,
    FeedImageSerializer,
    FeedActionSerializer,
    FeedActionCommentSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from CODE.utils.s3 import upload_image


class FeedView(ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()
    permission_classes = [IsAuthenticated,]

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_verified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_verified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_verified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = {
            'subject': request.data.get('subject'),
            'body': request.data.get('body'),
            'user': current_user.id
        }
        serializer = FeedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_verified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        feed = Feed.objects.get(id=kwargs.get('pk'))
        if feed.user.id != current_user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = FeedSerializer(feed)
        serializer.update(feed, data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_verified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        feed = Feed.objects.get(id=kwargs.get('pk'))
        if feed.user.id != current_user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = FeedSerializer(feed)
        serializer.update(feed, data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_verified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        feed = Feed.objects.get(id=kwargs.get('pk'))
        if feed.user.id != current_user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        feed.isActive = False
        feed.save()
        return Response({'message': 'Feed deleted successfully'}, status=status.HTTP_200_OK)


class FeedImageView(ModelViewSet):
    serializer_class = FeedImageSerializer
    queryset = FeedImage.objects.all()
    permission_classes = [IsAuthenticated,]
    search_fields = ['feed__subject', 'feed__body', 'feed__user__name']
    ordering = ('-createdAt',)

    def create(self, request, *args, **kwargs):
        img_file = request.FILES.get('file', None)
        if img_file is None:
            return Response("file is required", status=status.HTTP_400_BAD_REQUEST)
        img_url = upload_image(img_file)
        data = {
            'feed': request.data.get('feed'),
            'image': img_url,
            'coverImage': request.data.get('coverImage', False),
        }
        serialized_data = FeedImageSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if 'coverImage' in request.data:
            instance = self.get_object()
            self.get_queryset().filter(feed=instance.feed.id).update(coverImage=False)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if 'coverImage' in request.data:
            instance = self.get_object()
            self.get_queryset().filter(feed=instance.feed.id).update(coverImage=False)
        return super().partial_update(request, *args, **kwargs)


class FeedActionView(ModelViewSet):
    serializer_class = FeedActionSerializer
    queryset = FeedAction.objects.all()
    permission_classes = [IsAuthenticated,]
    search_fields = ['feed__subject', 'feed__body', 'feed__user__name']
    ordering = ('-createdAt',)


class FeedActionCommentView(ModelViewSet):
    serializer_class = FeedActionCommentSerializer
    queryset = FeedActionComment.objects.all()
    permission_classes = [IsAuthenticated,]
    search_fields = ['feedAction__feed__subject', 'feedAction__feed__body', 'feedAction__feed__user__name']
