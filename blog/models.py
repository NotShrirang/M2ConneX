from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser
from django.utils.translation import gettext_lazy as _


class Blog(CODEBaseModel):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200, null=False, db_column="title")
    content = models.TextField(verbose_name=_("Content"),
                               null=False, db_column="content")
    author = models.ForeignKey(verbose_name=_("Author"),
                               to=AlumniPortalUser, on_delete=models.CASCADE, db_column="author_id", related_name="blogs")
    keywords = models.CharField(verbose_name=_("Keywords"), max_length=200,
                                null=True, db_column="keywords")
    image = models.URLField(verbose_name=_(
        "Image"), null=True, db_column="image")
    isPublic = models.BooleanField(verbose_name=_("Is Public"),
                                   null=False, default=True, db_column="is_public")
    isDrafted = models.BooleanField(verbose_name=_("Is Drafted"),
                                    null=False, default=False, db_column="is_drafted")

    def __str__(self):
        return self.title + " by " + self.author.firstName + " " + self.author.lastName

    class Meta:
        db_table = "blog"
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        managed = True


class BlogAction(CODEBaseModel):

    ACTION_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('comment', 'comment'),
        ('report', 'report'),
    )

    action = models.CharField(verbose_name=_("Action"), max_length=10,
                              choices=ACTION_CHOICES, null=False, db_column="action")
    user = models.ForeignKey(verbose_name=_("User"),
                             to=AlumniPortalUser, on_delete=models.CASCADE, db_column="user_id", related_name="user_blog_actions")
    blog = models.ForeignKey(verbose_name=_("Blog"),
                             to=Blog, on_delete=models.CASCADE, db_column="blog_id", related_name="actions")

    def __str__(self):
        return self.action + " by " + self.user.firstName + " " + self.user.lastName

    class Meta:
        db_table = "blog_action"
        verbose_name = _("Blog Action")
        verbose_name_plural = _("Blog Actions")
        managed = True


class BlogComment(CODEBaseModel):
    comment = models.TextField(verbose_name=_("Content"),
                               null=False, db_column="content")
    user = models.ForeignKey(verbose_name=_("User"),
                             to=AlumniPortalUser, on_delete=models.CASCADE, db_column="author_id", related_name="user_blog_comments")
    action = models.ForeignKey(verbose_name=_("action"),
                               to=BlogAction, on_delete=models.CASCADE, db_column="blog_action_id", related_name="comments")

    def __str__(self):
        try:
            return self.comment[:20]
        except IndexError:
            return self.comment

    class Meta:
        db_table = "blog_comment"
        verbose_name = _("Blog Comment")
        verbose_name_plural = _("Blog Comments")
        managed = True
