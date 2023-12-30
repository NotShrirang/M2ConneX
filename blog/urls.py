from django.urls import path
from rest_framework import routers
from .views import BlogView, BlogCommentView, BlogActionView, BlogDislikeView

router = routers.DefaultRouter()
router.register('blog', BlogView, basename='blog')
router.register('blog-comment', BlogCommentView, basename='blog-comment')
router.register('blog-action', BlogActionView, basename='blog-action')

urlpatterns = [
    path('blog-dislike/', BlogDislikeView.as_view(), name='blog-dislike'),
]
urlpatterns += router.urls
