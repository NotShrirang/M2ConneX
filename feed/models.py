from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser

class Feed(CODEBaseModel):
    subject = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    images = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'feed'

    def __str__(self):
        return self.subject
    
    def get_images(self):
        pass

class FeedAction(CODEBaseModel):

    FEED_ACTIONS = (
        ('LIKE', 'Like'),
        ('SHARE', 'Share'),
        ('COMMENT', 'Comment'),
    )

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='feed_actions')
    action = models.CharField(max_length=10, choices=FEED_ACTIONS, null=False, blank=False)
    user = models.ForeignKey(AlumniPortalUser, on_delete=models.CASCADE, related_name='feed_actions')

    class Meta:
        ordering = ['-createdAt']
        db_table = 'feed_action'

    def __str__(self):
        return self.action
