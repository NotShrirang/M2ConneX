from feed.views import (
    FeedView,
    FeedActionView,
    FeedActionDislikeView,
    FeedImageView,
    FeedActionCommentView,
    UserActivityView,
    RecommendFeedView
)
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Feed API',
            'endpoints': [
                '/feed/',
                '/feed/recommend-feed/',
                '/feed-action/',
                '/feed-image/',
                '/feed-action-comment/',
                '/feed-action-dislike/'
            ]
        })


router = SimpleRouter()
router.register('feed', FeedView, basename='feed')
router.register('feed-action', FeedActionView, basename='feed-action')
router.register('feed-image', FeedImageView, basename='feed-image')
router.register('feed-action-comment', FeedActionCommentView,
                basename='feed-action-comment')

urlpatterns = [
    path('', HomeView.as_view()),
    path('user-activity/', UserActivityView.as_view()),
    path('recommend-feed/', RecommendFeedView.as_view()),
    path('feed-action-dislike/', FeedActionDislikeView.as_view())
] + router.urls
