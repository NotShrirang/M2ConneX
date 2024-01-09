from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status, filters, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BlogSerializer, BlogCommentSerializer, BlogActionSerializer
from .models import Blog, BlogComment, BlogAction
from .filters import BlogFilter, BlogCommentFilter, BlogActionFilter

from connection.models import Connection


class BlogView(ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filterset_class = BlogFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
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

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        qs = self.filter_queryset(self.get_queryset())
        qs = qs.filter(isPublic=True, isDrafted=False)
        print(qs, flush=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BlogSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        data['author'] = current_user.id
        serializer = BlogSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'blog' not in data:
            return Response({'message': 'Blog is required'}, status=status.HTTP_400_BAD_REQUEST)
        if 'action' not in data:
            return Response({'message': 'Action is required'}, status=status.HTTP_400_BAD_REQUEST)
        data['user'] = current_user.id
        serializer = BlogActionSerializer(data=data)
        if serializer.is_valid():
            if data['action'] == 'comment':
                if 'comment' not in data:
                    return Response({'message': 'Comment is required'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            final_data = serializer.data
            if data['action'] == 'comment':
                comment_data = {
                    'comment': data['comment'],
                    'user': current_user.id,
                    'action': serializer.data['id']
                }
                comment_serializer = BlogCommentSerializer(data=comment_data)
                if comment_serializer.is_valid():
                    comment_serializer.save()
                    final_data['comment'] = comment_serializer.data
                else:
                    actionId = serializer.data['id']
                    BlogAction.objects.get(id=actionId).delete()
                    return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(final_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDislikeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'blog' not in data:
            return Response({'message': 'Blog is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            blog = Blog.objects.get(id=data['blog'])
        except Blog.DoesNotExist:
            return Response({'message': 'Blog does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        action = BlogAction.objects.filter(
            action='like', user=current_user, blog=blog)
        if action.exists():
            action.delete()
            return Response({'message': 'Blog like removed'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Blog is not liked'}, status=status.HTTP_400_BAD_REQUEST)


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
