from connection.views import (
    ConnectionViewSet,
    ConnectionRequestView,
    ConnectionRequestAcceptView,
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
                '/connection-request/',
                '/connection-request-accept/',
            ]
        })

router = SimpleRouter()
router.register('connection', ConnectionViewSet)

urlpatterns = [
    path('', HomeView.as_view()),
    path('connection-request/', ConnectionRequestView.as_view()),
    path('connection-request-accept/', ConnectionRequestAcceptView.as_view()),
] + router.urls