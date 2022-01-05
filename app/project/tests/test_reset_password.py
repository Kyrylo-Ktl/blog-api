import pytest
import secrets
from django.urls import reverse

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from django.core import mail
from scripts.seed_db import get_random_password
from .helpers import sending_reset_password_email
from .conftest import fake, PASSWORD_RESET_REQUEST_URL


@pytest.mark.django_db
def test_post_request_password_reset_for_invalid_email(anonymous_client):
    client, _ = anonymous_client
    response = client.post(PASSWORD_RESET_REQUEST_URL, data={'email': 'invalid_email'})

    assert HTTP_400_BAD_REQUEST == response.status_code
    assert 0 == len(mail.outbox)
    assert ['Enter a valid email address.'] == response.json().get('email')


@pytest.mark.django_db
def test_post_request_password_reset_for_non_existent_email(anonymous_client):
    client, _ = anonymous_client
    response = client.post(PASSWORD_RESET_REQUEST_URL, data={'email': fake.email()})

    assert HTTP_400_BAD_REQUEST == response.status_code
    assert 0 == len(mail.outbox)
    assert ['No user with such email.'] == response.json().get('email')


@pytest.mark.django_db
def test_post_request_password_reset(authorized_client):
    client, user = authorized_client
    response = client.post(PASSWORD_RESET_REQUEST_URL, data={'email': user.email})

    sending_reset_password_email(user)
    assert HTTP_200_OK == response.status_code
    assert 'We have sent you a link to reset your password' == response.json().get('success')


@pytest.mark.django_db
def test_get_confirm_password_reset_with_invalid_token(anonymous_client):
    client, _ = anonymous_client
    kwargs = {
        'uuid': secrets.token_hex(2),
        'token': secrets.token_hex(16),
    }
    response = client.get(reverse('confirm-reset', kwargs=kwargs))

    assert HTTP_400_BAD_REQUEST == response.status_code
    assert 'Token is not valid, please request a new one' == response.json().get('error')


@pytest.mark.django_db
def test_get_confirm_password_reset(authorized_client):
    client, user = authorized_client
    kwargs = {
        'uuid': user.get_uuid(),
        'token': user.get_password_reset_token(),
    }
    response = client.get(reverse('confirm-reset', kwargs=kwargs))

    assert HTTP_200_OK == response.status_code
    assert 'Token is valid, use POST to change password.' == response.json().get('success')


@pytest.mark.django_db
def test_post_confirm_password_reset_with_invalid_token(anonymous_client):
    client, _ = anonymous_client
    kwargs = {
        'uuid': secrets.token_hex(2),
        'token': secrets.token_hex(16),
    }
    password = get_random_password()
    response = client.post(reverse('confirm-reset', kwargs=kwargs), data={'password': password})

    assert HTTP_400_BAD_REQUEST == response.status_code
    assert 'Token is not valid, please request a new one' == response.json().get('error')


@pytest.mark.django_db
def test_post_confirm_password_reset(authorized_client, password):
    client, user = authorized_client
    kwargs = {
        'uuid': user.get_uuid(),
        'token': user.get_password_reset_token(),
    }
    new_password = get_random_password()
    response = client.post(reverse('confirm-reset', kwargs=kwargs), data={'password': new_password})

    assert HTTP_200_OK == response.status_code
    assert 'Password has been changed successfully.' == response.json().get('success')
    user.refresh_from_db()
    assert not user.check_password(password)
    assert user.check_password(new_password)
