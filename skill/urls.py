from skill.views import (
    SkillView,
    UserSkillView,
    UserSkillByUserView
)
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Skill API',
            'endpoints': [
                '/skill/',
                '/user-skill/',
                '/user-skill-by-user/<uuid:userId>/'
            ]
        })


router = SimpleRouter()
router.register('skill', SkillView, basename='skill')
router.register('user-skill', UserSkillView, basename='user-skill')

urlpatterns = [
    path('', HomeView.as_view()),
    path('user-skill-by-user/<uuid:userId>/', UserSkillByUserView.as_view())
] + router.urls
