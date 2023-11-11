from feed.views import (
    FeedViewSet,
    FeedActionViewSet
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
                '/feedaction/',
            ]
        })


router = SimpleRouter()
router.register('feed', FeedViewSet)
router.register('feedaction', FeedActionViewSet)

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls
