from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import validate_password


class User(AbstractUser):
    password = models.CharField(max_length=128,
                                validators=[validate_password])
    first_name = models.CharField(max_length=64, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=64, validators=[MinLengthValidator(2)])

    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
