from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from experience.views import ExperienceView, UserExperienceView


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Experience API',
            'endpoints': [
                '/experience/',
                '/user-experience/<uuid:userId>/',
            ]
        })


router = SimpleRouter()
router.register('experience', ExperienceView, basename='experience')

urlpatterns = [
    path('', HomeView.as_view()),
    path('user-experience/<uuid:userId>/', UserExperienceView.as_view()),
] + router.urls
