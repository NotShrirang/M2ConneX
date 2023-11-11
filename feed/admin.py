from django.contrib import admin
from .models import (
    Feed,
    FeedImage,
    FeedAction,
    FeedActionComment,
)


admin.site.register(Feed)
admin.site.register(FeedImage)
admin.site.register(FeedAction)
admin.site.register(FeedActionComment)
