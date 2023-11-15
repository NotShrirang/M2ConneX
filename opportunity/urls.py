from opportunity.views import (
    OpportunityView,
    OpportunitySkillView,
    OpportunityApplicationView,
    AcceptOpportunityApplication,
    RejectOpportunityApplication,
    RecommendOpportunityView
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
                '/opportunity-application/',
                '/accept-opportunity-application/',
                '/reject-opportunity-application/',
                '/recommend-opportunity/'
            ]
        })

router = SimpleRouter()
router.register('opportunity', OpportunityView, basename='opportunity')
router.register('opportunity-skill', OpportunitySkillView, basename='opportunity-skill')
router.register('opportunity-application', OpportunityApplicationView, basename='opportunity-application')

urlpatterns = [
    path('', HomeView.as_view()),
    path('accept-opportunity-application/', AcceptOpportunityApplication.as_view()),
    path('reject-opportunity-application/', RejectOpportunityApplication.as_view()),
    path('recommend-opportunity/', RecommendOpportunityView.as_view())
] + router.urls