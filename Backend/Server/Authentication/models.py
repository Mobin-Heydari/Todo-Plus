from django.db import models

from Users.models import User



class OneTimePassword(models.Model):
    # User who requested the OTP
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='one_time_passwords',
    )

    # Field to store a unique token for the OTP
    token = models.CharField(max_length=250, unique=True)
    
    code = models.CharField(max_length=6)  # Field to store the OTP code

    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the OTP is created
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the OTP is last updated

    class Meta:
        verbose_name = 'One Time Password'
        verbose_name_plural = 'One Time Passwords'

    
    def __str__(self):
        return f'user: {self.user.username}, code: {self.code}'
    