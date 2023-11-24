from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import BlogSerializer, BlogCommentSerializer, BlogActionSerializer
from .models import Blog, BlogComment, BlogAction
from .filters import BlogFilter, BlogCommentFilter, BlogActionFilter


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filterset_class = BlogFilter
    permission_classes = [IsAuthenticated]
    search_fields = [
        'title',
        'content',
        'author__user__firstName',
        'author__user__lastName',
        'author__user__email',
    ]
    ordering_fields = [
        'author__user__firstName',
        'author__user__lastName',
        'author__user__email',
        'isPublic',
        'isDrafted',
        'createdAt',
        'updatedAt',
    ]
    ordering = ['-createdAt']


class BlogCommentViewSet(ModelViewSet):
    serializer_class = BlogCommentSerializer
    queryset = BlogComment.objects.all()
    filterset_class = BlogCommentFilter
    permission_classes = [IsAuthenticated]
    search_fields = [
        'comment',
        'user__user__firstName',
        'user__user__lastName',
        'user__user__email',
        'blog__title',
        'blog__content',
        'blog__author__user__firstName',
        'blog__author__user__lastName',
        'blog__author__user__email',
    ]
    ordering_fields = [
        'user__user__firstName',
        'user__user__lastName',
        'user__user__email',
        'blog__title',
        'createdAt',
        'updatedAt',
    ]
    ordering = ['-createdAt']


class BlogActionViewSet(ModelViewSet):
    serializer_class = BlogActionSerializer
    queryset = BlogAction.objects.all()
    filterset_class = BlogActionFilter
    permission_classes = [IsAuthenticated]
    search_fields = [
        'action',
        'user__user__firstName',
        'user__user__lastName',
        'user__user__email',
        'blog__title',
        'blog__content',
        'blog__author__user__firstName',
        'blog__author__user__lastName',
        'blog__author__user__email',
    ]
    ordering_fields = [
        'user__user__firstName',
        'user__user__lastName',
        'user__user__email',
        'blog__title',
        'createdAt',
        'updatedAt',
    ]
    ordering = ['-createdAt']
