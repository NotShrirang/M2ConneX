from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from experience.views import ExperienceViewSet

router = SimpleRouter()
router.register('experience', ExperienceViewSet)

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Experience API',
            'endpoints': [
                '/experience/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls