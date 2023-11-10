from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser

class Skill(CODEBaseModel):

    EXPERIENCE_CHOICES = (
        ('Interested', 'Interested'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
        ('Gawd', 'Gawd'),
    )
    name = models.CharField(max_length=100, null=False, blank=False)
    experience = models.CharField(max_length=100, null=False, blank=False, choices=EXPERIENCE_CHOICES)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'skill'

    def __str__(self):
        return self.name
    
class UserSkill(CODEBaseModel):
    user = models.ForeignKey(AlumniPortalUser, on_delete=models.CASCADE, related_name='user_skills')
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills_list')

    class Meta:
        ordering = ['-createdAt']
        db_table = 'user_skill'

    def __str__(self):
        return self.user.name + ' - ' + self.skills.name