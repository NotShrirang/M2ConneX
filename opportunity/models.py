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

    WORK_MODE_CHOICES = (
        ('Remote', 'Remote'),
        ('In Office', 'In Office'),
        ('Hybrid', 'Hybrid'),
    )

    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    payPerMonth = models.IntegerField(null=True, blank=True)
    isPaid = models.BooleanField(null=False, blank=False, default=True)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='opportunities')
    type = models.CharField(max_length=100, null=False, blank=False, choices=OPPORTUNITY_CHOICES)
    companyName = models.CharField(max_length=100, null=False, blank=False)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    workMode = models.CharField(max_length=100, null=True, blank=True, choices=WORK_MODE_CHOICES, default='Hybrid')

    class Meta:
        ordering = ['-createdAt']
        db_table = 'opportunity'
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"

    def __str__(self):
        return self.name


class OpportunitySkill(CODEBaseModel):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='opportunities')

    class Meta:
        ordering = ['-createdAt']
        db_table = 'opportunity_skill'
        verbose_name = "Opportunity Skill"
        verbose_name_plural = "Opportunity Skills"

    def __str__(self):
        return self.opportunity.name + ' - ' + self.skill.name


class OpportunityApplication(CODEBaseModel):

    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('ACCEPTED', 'ACCEPTED'),
        ('REJECTED', 'REJECTED'),
    )

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='opportunity_applications')
    about = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=False, blank=False, default='PENDING')
    
    class Meta:
        ordering = ['-createdAt']
        db_table = 'opportunity_application'
        verbose_name = "Opportunity Application"
        verbose_name_plural = "Opportunity Applications"

    def __str__(self):
        return self.opportunity.name + ' - ' + self.applicant.user.email