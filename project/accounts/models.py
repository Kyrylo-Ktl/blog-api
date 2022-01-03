"""The module is used to describe database models"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from snippets.helpers import reverse_external


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

    def get_uuid(self):
        uuid = urlsafe_base64_encode(smart_bytes(self.id))
        return uuid

    def get_password_reset_token(self):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        return token

    def get_password_reset_url(self):
        reset_url = reverse_external(
            'confirm-reset',
            uuid=self.get_uuid(),
            token=self.get_password_reset_token()
        )
        return reset_url

    @classmethod
    def get_by_uuid(cls, uuid: str):
        user_id = smart_str(urlsafe_base64_decode(uuid))
        user = cls.objects.get(id=user_id)
        return user

    @classmethod
    def is_valid_password_reset_token(cls, uuid: str, token: str) -> bool:
        token_generator = PasswordResetTokenGenerator()
        try:
            user = cls.get_by_uuid(uuid)
            return token_generator.check_token(user, token)
        except (ValueError, DjangoUnicodeDecodeError):
            return False

    def send_password_reset_mail(self):
        self.email_user(
            subject='Reset your password',
            message=self.get_password_reset_url(),
        )
