from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class Skill(CODEBaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'skill'
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name


class UserSkill(CODEBaseModel):

    EXPERIENCE_CHOICES = (
        ('1', 'Interested'),
        ('2', 'Beginner'),
        ('3', 'Intermediate'),
        ('4', 'Expert'),
        ('5', 'Gawd'),
    )

    user = models.ForeignKey(
        AlumniPortalUser, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='users')
    experience = models.CharField(
        max_length=100, null=False, blank=False, choices=EXPERIENCE_CHOICES)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'user_skill'
        verbose_name = "User Skill"
        verbose_name_plural = "User Skills"

    def __str__(self):
        return self.user.email + ' - ' + str(self.skill.name)
