from django.db import models
from CODE.models import CODEBaseModel
from users.models import Blogger, AlumniPortalUser
from django.utils.translation import gettext_lazy as _


class Blog(CODEBaseModel):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100, null=False, db_column="title")
    content = models.TextField(verbose_name=_("Content"),
                               null=False, db_column="content")
    author = models.ForeignKey(verbose_name=_("Author"),
                               to=Blogger, on_delete=models.CASCADE, db_column="author_id", related_name="blogs")
    isPublic = models.BooleanField(verbose_name=_("Is Public"),
                                   null=False, default=True, db_column="is_public")
    isDrafted = models.BooleanField(verbose_name=_("Is Drafted"),
                                    null=False, default=False, db_column="is_drafted")

    def __str__(self):
        return self.title + " by " + self.author.user.firstName + " " + self.author.user.lastName

    class Meta:
        db_table = "blog"
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        managed = True


class BlogComment(CODEBaseModel):
    comment = models.TextField(verbose_name=_("Content"),
                               null=False, db_column="content")
    user = models.ForeignKey(verbose_name=_("User"),
                             to=AlumniPortalUser, on_delete=models.CASCADE, db_column="author_id", related_name="user_blog_comments")
    blog = models.ForeignKey(verbose_name=_("Blog"),
                             to=Blog, on_delete=models.CASCADE, db_column="blog_id", related_name="comments")

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


class BlogAction(CODEBaseModel):

    ACTION_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('report', 'Report'),
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
