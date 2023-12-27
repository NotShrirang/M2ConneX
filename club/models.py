from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class Club(CODEBaseModel):
    name = models.CharField(max_length=100, unique=True,
                            null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    logo = models.URLField(max_length=200, null=False)
    website = models.URLField(max_length=200, null=True, blank=True)
    socialMedia1 = models.URLField(max_length=200, null=True, blank=True)
    socialMedia2 = models.URLField(max_length=200, null=True, blank=True)
    socialMedia3 = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'club'
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'
        managed = True

    def __str__(self):
        return self.name


class ClubMember(CODEBaseModel):
    POSITION_CHOICES = (
        ('faculty_mentor', 'faculty_mentor'),
        ('head', 'head'),
        ('core_member', 'core_member'),
        ('member', 'member'),
    )
    user = models.ForeignKey(
        AlumniPortalUser, on_delete=models.CASCADE, null=False, related_name='clubs')
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, null=False, related_name='members')
    position = models.CharField(
        choices=POSITION_CHOICES, max_length=100, null=False)
    positionInWords = models.CharField(max_length=100, null=False)
    isClubAdmin = models.BooleanField(default=False)

    class Meta:
        db_table = 'club_member'
        verbose_name = 'Club Member'
        verbose_name_plural = 'Club Members'
        unique_together = ('user', 'club')
        managed = True

    def __str__(self):
        return f'{self.club.name} - {self.user}'
