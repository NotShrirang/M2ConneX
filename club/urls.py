from rest_framework.routers import DefaultRouter

from .views import ClubView, ClubMemberView

router = DefaultRouter()
router.register(r'club', ClubView, basename='club')
router.register(r'club-member', ClubMemberView, basename='club-member')

urlpatterns = []
urlpatterns += router.urls
