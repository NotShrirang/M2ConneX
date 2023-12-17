from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser
from django.utils.translation import gettext_lazy as _


class Feed(CODEBaseModel):
    subject = models.CharField(verbose_name=_('Subject'), max_length=100, null=False, blank=False)
    body = models.TextField(verbose_name=_('Body'), null=False, blank=False)  # TODO: Add Rich Text Field
    user = models.ForeignKey(AlumniPortalUser, verbose_name=_('User'), on_delete=models.CASCADE, related_name='feed')
    isPublic = models.BooleanField(verbose_name=_('Is Public'), default=True)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'feed'
        verbose_name = _('Feed')
        verbose_name_plural = _('Feed')

    def __str__(self):
        return self.subject


class FeedImage(CODEBaseModel):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(null=False, blank=False)
    coverImage = models.BooleanField(default=False)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'feed_image'
        verbose_name = _('Feed Image')
        verbose_name_plural = _('Feed Images')

    def __str__(self):
        return self.image


class FeedAction(CODEBaseModel):

    FEED_ACTIONS = (
        ('LIKE', 'Like'),
        ('SHARE', 'Share'),
        ('COMMENT', 'Comment'),
    )

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=10, choices=FEED_ACTIONS, null=False, blank=False)
    user = models.ForeignKey(AlumniPortalUser, on_delete=models.CASCADE, related_name='feed_actions')

    class Meta:
        ordering = ['-createdAt']
        db_table = 'feed_action'
        verbose_name = _('Feed Action')
        verbose_name_plural = _('Feed Actions')

    def __str__(self):
        return self.action


class FeedActionComment(CODEBaseModel):
    feedAction = models.ForeignKey(FeedAction, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'feed_action_comment'
        verbose_name = _('Feed Action Comment')
        verbose_name_plural = _('Feed Action Comments')

    def __str__(self):
        return (self.feedAction.user.firstName or "") + (self.feedAction.user.lastName or "") + " - " + self.comment[:20] + "..."
