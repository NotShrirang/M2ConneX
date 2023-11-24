from CODE.filters import CODEDateFilter
from .models import Blog, BlogComment, BlogAction


class BlogFilter(CODEDateFilter):
    class Meta:
        model = Blog
        fields = (
            'createdAt',
            'updatedAt',
            'isPublic',
            'isDrafted',
            'author'
        )


class BlogCommentFilter(CODEDateFilter):
    class Meta:
        model = BlogComment
        fields = (
            'createdAt',
            'updatedAt',
            'user',
            'blog'
        )


class BlogActionFilter(CODEDateFilter):
    class Meta:
        model = BlogAction
        fields = (
            'createdAt',
            'updatedAt',
            'action',
            'user',
            'blog'
        )
