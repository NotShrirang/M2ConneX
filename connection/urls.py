from connection.views import (
    ConnectionView,
    ConnectionRequestView,
    ConnectionRequestAcceptView,
    ConnectionRequestRejectView,
    RecommendConnectionView
)
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Connection API',
            'endpoints': [
                '/connection/',
                '/connection/recommend-connection',
                '/connection-request/',
                '/connection-request-accept/',
                '/connection-request-reject/',
            ]
        })


router = SimpleRouter()
router.register('connection', ConnectionView, basename='connection')

urlpatterns = [
    path('', HomeView.as_view()),
    path('recommend-connection/', RecommendConnectionView.as_view()),
    path('connection-request/', ConnectionRequestView.as_view()),
    path('connection-request-accept/', ConnectionRequestAcceptView.as_view()),
    path('connection-request-reject/', ConnectionRequestRejectView.as_view()),
] + router.urls
