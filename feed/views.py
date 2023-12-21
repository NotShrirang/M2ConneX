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
    FeedActionCommentSerializer,
    UserActivitySerializer
)
from feed.filters import (
    FeedFilter,
    FeedActionFilter,
    FeedActionCommentFilter,
    FeedImageFilter
)
from connection.models import Connection
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, views, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from itertools import chain

from CODE.utils.s3 import upload_image
from CODE.utils.recommendations import get_feed_recommendation
from analytics.models import UserAnalytics
from analytics.serializers import UserAnalyticsSerializer


class FeedView(ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()
    filterset_class = FeedFilter
    permission_classes = [IsAuthenticated,]
    ordering = ('-createdAt',)

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        qs = self.queryset.filter(isActive=True)
        userA_connected = Connection.objects.filter(
            userA=current_user, status='accepted').values_list('userB', flat=True)
        userB_connected = Connection.objects.filter(
            userB=current_user, status='accepted').values_list('userA', flat=True)
        qs = qs.exclude(user=current_user.id)
        qs = qs.filter(Q(user__in=userA_connected) | Q(
            user__in=userB_connected) | Q(isPublic=True)).order_by('-createdAt')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = FeedSerializer(
                page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = {
            'subject': request.data.get('subject'),
            'body': request.data.get('body'),
            'user': current_user.id
        }
        serializer = FeedSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            final_data = serializer.data
            feedId = serializer.data['id']
            images = request.data.get('images', [])
            final_image_data = []
            for image in images:
                if image == images[0]:
                    image_data = {
                        'feed': feedId.replace('"', '').replace("'", ""),
                        'image': image,
                        'coverImage': True
                    }
                else:
                    image_data = {
                        'feed': feedId.replace('"', '').replace("'", ""),
                        'image': image,
                        'coverImage': False
                    }
                print(image_data)
                if image_data['feed'] == '' or image_data['feed'] == None:
                    return Response({'message': 'Feed is required'}, status=status.HTTP_400_BAD_REQUEST)
                feedImage = FeedImage.objects.create(feed=Feed.objects.get(
                    id=image_data['feed']), image=image_data['image'], coverImage=image_data['coverImage'])
                image_serializer = FeedImageSerializer(feedImage)
                final_image_data.append(image_serializer.data)
            final_data['images'] = final_image_data
            return Response(final_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = {
            'subject': request.data.get('subject'),
            'body': request.data.get('body'),
            'user': current_user
        }
        feed = Feed.objects.get(id=kwargs.get('pk'))
        if feed.user.id != current_user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = FeedSerializer(feed, context={'request': request})
        serializer.update(feed, data)
        feedImageQs = FeedImage.objects.filter(
            feed=Feed.objects.get(id=kwargs.get('pk'))).order_by('createdAt')
        if feedImageQs.exists():
            for feedImage in feedImageQs:
                feedImage.delete()
        final_data = serializer.data
        feedId = serializer.data['id']
        images = request.data.get('images', [])
        final_image_data = []
        for image in images:
            if image == images[0]:
                image_data = {
                    'feed': feedId.replace('"', '').replace("'", ""),
                    'image': image,
                    'coverImage': True
                }
            else:
                image_data = {
                    'feed': feedId.replace('"', '').replace("'", ""),
                    'image': image,
                    'coverImage': False
                }
            if image_data['feed'] == '' or image_data['feed'] == None:
                return Response({'message': 'Feed is required'}, status=status.HTTP_400_BAD_REQUEST)
            feedImage = FeedImage.objects.create(feed=Feed.objects.get(
                id=image_data['feed']), image=image_data['image'], coverImage=image_data['coverImage'])
            image_serializer = FeedImageSerializer(feedImage)
            final_image_data.append(image_serializer.data)
            final_data['images'] = final_image_data
        return Response(final_data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
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
        if not current_user.isVerified:
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
    filterset_class = FeedImageFilter
    permission_classes = [IsAuthenticated,]
    search_fields = ['feed__subject', 'feed__body', 'feed__user__name']
    ordering = ('-createdAt',)

    def list(self, request, *args, **kwargs):
        feed = request.query_params.get('feed', None)
        if feed is None:
            return Response({"message": "Feed is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            feed = Feed.objects.get(id=feed)
            if feed.user.id != request.user.id:
                return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
            qs = self.queryset.filter(feed=feed.id)
            if qs.exists():
                serializer = self.get_serializer(qs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        feed = request.query_params.get('feed', None)
        imageId = request.query_params.get('imageId', None)
        if feed is None or imageId is None:
            return Response({"message": "Feed is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            feed = Feed.objects.get(id=feed)
            if feed.user.id != request.user.id:
                return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
            qs = self.queryset.filter(feed=feed.id, id=imageId)
            if qs.exists():
                serializer = self.get_serializer(qs.first())
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        img_file = request.FILES.get('file', None)
        if img_file is None:
            return Response({'message': 'Image not found.'}, status=status.HTTP_404_BAD_REQUEST)
        img_url = upload_image(img_file)
        data = {
            'feed': request.data.get('feed'),
            'image': img_url,
            'coverImage': request.data.get('coverImage', False),
        }
        serialized = FeedImageSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.feed.user.id != request.user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        instance.isActive = False
        instance.save()
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)


class FeedActionView(ModelViewSet):
    serializer_class = FeedActionSerializer
    queryset = FeedAction.objects.all()
    filterset_class = FeedActionFilter
    permission_classes = [IsAuthenticated,]
    search_fields = ['feed__subject', 'feed__body', 'feed__user__name']
    ordering = ('-createdAt',)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        feedId = request.data.get('feed', None)
        action = request.data.get('action', None)
        if feedId is None:
            return Response({'message': 'feed is required'}, status=status.HTTP_400_BAD_REQUEST)
        if action is None:
            return Response({'message': 'action is required'}, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'feed': feedId,
            'action': action,
            'user': current_user.id
        }
        if action == 'LIKE':
            if FeedAction.objects.filter(feed=feedId, user=current_user.id, action='LIKE').exists():
                return Response({'message': 'You have already liked this feed'}, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'COMMENT':
            data['comment'] = request.data.get('comment', None)
            if data['comment'] is None:
                return Response({'message': 'comment is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FeedActionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            final_data = serializer.data
            if action == 'LIKE':
                analytics_data = {
                    'profileUser': Feed.objects.get(id=feedId).user.id,
                    'visitor': current_user.id,
                    'analyticsType': 'feed like'
                }
            elif action == 'COMMENT':
                comment_data = {
                    'feedAction': serializer.data['id'],
                    'comment': data['comment'],
                }
                comment_serializer = FeedActionCommentSerializer(
                    data=comment_data)
                if comment_serializer.is_valid():
                    comment_serializer.save()
                    analytics_data = {
                        'profileUser': Feed.objects.get(id=feedId).user.id,
                        'visitor': current_user.id,
                        'analyticsType': 'feed comment'
                    }
                else:
                    return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                final_data['comment'] = comment_serializer.data
            elif action == 'SHARE':
                analytics_data = {
                    'profileUser': Feed.objects.get(id=feedId).user.id,
                    'visitor': current_user.id,
                    'analyticsType': 'feed share'
                }
            analytics_serializer = UserAnalyticsSerializer(
                data=analytics_data)
            if analytics_serializer.is_valid():
                analytics_serializer.save()
            else:
                return Response(analytics_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(final_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        feedAction = FeedAction.objects.get(id=kwargs.get('pk'))
        if feedAction.user.id != request.user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        feedAction = FeedAction.objects.get(id=kwargs.get('pk'))
        if feedAction.user.id != request.user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Method not supported.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FeedActionDislikeView(views.APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        current_user = request.user
        feedId = request.data.get('feed', None)
        if feedId is None:
            return Response({'message': 'feedAction is required'}, status=status.HTTP_400_BAD_REQUEST)
        feedAction = FeedAction.objects.get(
            feed=feedId, user=current_user.id, action='LIKE')
        if feedAction.user.id != request.user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        feedAction.delete()
        return Response({'message': 'Feed action deleted successfully'}, status=status.HTTP_200_OK)


class FeedActionCommentView(ModelViewSet):
    serializer_class = FeedActionCommentSerializer
    queryset = FeedActionComment.objects.all()
    filterset_class = FeedActionCommentFilter
    permission_classes = [IsAuthenticated,]
    search_fields = ['feedAction__feed__subject',
                     'feedAction__feed__body', 'feedAction__feed__user__name']
    ordering = ('-createdAt',)

    def list(self, request, *args, **kwargs):
        feed = request.query_params.get('feed', None)
        if feed is None:
            return Response({"message": "feed is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            feedActions = FeedAction.objects.filter(
                feed=feed, action='COMMENT')
            qs = FeedActionComment.objects.filter(feedAction__in=feedActions)
            if qs.exists():
                serializer = FeedActionCommentSerializer(qs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Comments not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        return Response({'message': 'Method not supported.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'Method not supported.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'Method not supported.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        feedActionComment = FeedActionComment.objects.get(id=kwargs.get('pk'))
        if feedActionComment.feedAction.user.id != request.user.id:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        feedActionComment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_200_OK)


class UserActivityView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    pagination_class = pagination.PageNumberPagination
    page_size = 10

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        feed_action_queryset = FeedAction.objects.filter(user=current_user)
        feed_queryset = Feed.objects.filter(user=current_user)

        combined_queryset = sorted(
            chain(feed_queryset, feed_action_queryset),
            key=lambda instance: instance.createdAt,
            reverse=True
        )

        paginated_queryset = self.paginate_queryset(combined_queryset)

        serialized_data = UserActivitySerializer(
            paginated_queryset, context={'request': request}, many=True).data

        return self.get_paginated_response(serialized_data)


class RecommendFeedView(generics.ListAPIView):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()
    filterset_class = FeedFilter
    permission_classes = [IsAuthenticated,]
    search_fields = ['subject', 'body', 'user__email',
                     'user__firstName', 'user__lastName', 'user__department']
    ordering = ('-createdAt',)

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        # userA_connected = Connection.objects.filter(userA=current_user, status='accepted').values_list('userB', flat=True)
        # userB_connected = Connection.objects.filter(userB=current_user, status='accepted').values_list('userA', flat=True)
        # # qs = Feed.objects.filter(self.queryset.exclude(user=current_user.id))
        # qs =  Feed.objects.filter(Q(user__in=userA_connected) | Q(user__in=userB_connected) | Q(isPublic=True) | Q(user=current_user.id))
        # # Paginate the queryset
        # page = self.paginate_queryset(qs)
        # if page is not None:
        #     serializer = FeedSerializer(page, context={'request': request}, many=True)
        #     return self.get_paginated_response(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        userA_connected = Connection.objects.filter(
            userA=current_user, status='accepted').values_list('userB', flat=True)
        userB_connected = Connection.objects.filter(
            userB=current_user, status='accepted').values_list('userA', flat=True)
        qs = Feed.objects.filter(isActive=True)
        qs = qs.filter(Q(user__in=userA_connected) | Q(
            user__in=userB_connected) | Q(isPublic=True))
        qs, similarity_score = get_feed_recommendation(qs, current_user)
        # Paginate the queryset
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = FeedSerializer(
                page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
