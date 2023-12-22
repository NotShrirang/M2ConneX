from rest_framework import routers
from .views import BlogView, BlogCommentView, BlogActionView

router = routers.DefaultRouter()
router.register('blog', BlogView, basename='blog')
router.register('blog-comment', BlogCommentView, basename='blog-comment')
router.register('blog-action', BlogActionView, basename='blog-action')

urlpatterns = []
urlpatterns += router.urls
