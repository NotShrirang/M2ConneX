from django.db import models
from CODE.models import CODEBaseModel
from users.models import Alumni
from skill.models import Skill

class Opportunity(CODEBaseModel):

    OPPORTUNITY_CHOICES = (
        ('Job', 'Job'),
        ('Internship', 'Internship'),
        ('Scholarship', 'Scholarship'),
        ('Consultancy', 'Consultancy'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='opportunities')
    type = models.CharField(max_length=100, null=False, blank=False, choices=OPPORTUNITY_CHOICES)
    companyName = models.CharField(max_length=100, null=False, blank=False)
    startDate = models.DateField(null=False, blank=False)
    endDate = models.DateField(null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ['-createdAt']
        db_table = 'opportunity'

    def __str__(self):
        return self.name
    
class OpportunitySkill(CODEBaseModel):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='opportunity_skills')
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='opportunity_skills_list')

    class Meta:
        ordering = ['-createdAt']
        db_table = 'opportunity_skill'

    def __str__(self):
        return self.opportunity.name + ' - ' + self.skills.name