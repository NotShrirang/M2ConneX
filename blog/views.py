from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import BlogSerializer, BlogCommentSerializer, BlogActionSerializer
from .models import Blog, BlogComment, BlogAction
from .filters import BlogFilter, BlogCommentFilter, BlogActionFilter

from connection.models import Connection


class BlogView(ModelViewSet):
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


class BlogCommentView(ModelViewSet):
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


class BlogActionView(ModelViewSet):
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


class RecommendBlogView(generics.ListAPIView):
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
    ordering_fields = ('-createdAt', '-updatedAt', 'title')
    ordering = ['-createdAt']

    def list(self, request, *args, **kwargs):
        current_user = request.user

        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        qs = Blog.objects.filter(
            isPublic=True, isDrafted=False).exclude(author=current_user)
        userA_connected = Connection.objects.filter(
            userA=current_user, status='accepted').values_list('userB', flat=True)
        userB_connected = Connection.objects.filter(
            userB=current_user, status='accepted').values_list('userA', flat=True)

        