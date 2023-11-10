from opportunity.views import (
    OpportunityViewSet,
    OpportunitySkillViewSet
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
                '/opportunityskill/',
            ]
        })

router = SimpleRouter()
router.register('opportunity', OpportunityViewSet)
router.register('opportunityskill', OpportunitySkillViewSet)

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls