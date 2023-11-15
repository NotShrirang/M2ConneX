from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from experience.views import ExperienceView

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Experience API',
            'endpoints': [
                '/experience/',
            ]
        })

router = SimpleRouter()
router.register('experience', ExperienceView, basename='experience')

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls