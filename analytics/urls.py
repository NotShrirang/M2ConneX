from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import UserAnalyticsView, AnalyticsCountView


router = SimpleRouter()
router.register(r'analytics', UserAnalyticsView,
                basename='analytics')

urlpatterns = [
    path('analytics-count/', AnalyticsCountView.as_view(), name='analytics-count'),
]

urlpatterns += router.urls
