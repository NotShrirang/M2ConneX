from opportunity.views import (
    OpportunityView,
    OpportunitySkillView
)
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Opportunity API',
            'endpoints': [
                '/opportunity/',
                '/opportunity-skill/',
            ]
        })

router = SimpleRouter()
router.register('opportunity', OpportunityView, basename='opportunity')
router.register('opportunity-skill', OpportunitySkillView, basename='opportunity-skill')

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls