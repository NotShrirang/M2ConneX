from rest_framework import routers
from .views import BlogViewSet, BlogCommentViewSet, BlogActionViewSet

router = routers.DefaultRouter()
router.register('blog', BlogViewSet, basename='blog')
router.register('blog-comment', BlogCommentViewSet, basename='blog-comment')
router.register('blog-action', BlogActionViewSet, basename='blog-action')

urlpatterns = []
urlpatterns += router.urls
