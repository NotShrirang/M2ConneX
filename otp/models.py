from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class OTP(CODEBaseModel):
    """
    Model to store OTPs
    """
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(
        AlumniPortalUser, on_delete=models.CASCADE, related_name="otp", null=False, blank=False)
    isUsed = models.BooleanField(default=False)

    class Meta:
        db_table = "otp"
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        ordering = ['-createdAt']
        managed = True

    def __str__(self):
        return self.user.email + " - " + self.otp
