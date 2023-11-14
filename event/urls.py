from event.views import EventView, EventImageView
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Event API',
            'endpoints': [
                '/event/',
            ]
        })

router = SimpleRouter()
router.register('event', EventView, basename='event')
router.register('event-image', EventImageView, basename='event-image')

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls