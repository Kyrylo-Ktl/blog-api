import pytest
from typing import Dict

from django.core import mail
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

TOKEN_URL = reverse('tokens')


def authorize_client(client: APIClient, data: Dict) -> None:
    access_token = client.post(
        TOKEN_URL,
        data=data,
    ).json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')


@pytest.mark.django_db
def sending_reset_password_email(user):
    assert len(mail.outbox) == 1

    reset_mail = mail.outbox[0]
    assert reset_mail.subject == 'Reset your password'
    assert user.get_password_reset_url() in reset_mail.body
    assert reset_mail.to == [user.email]
