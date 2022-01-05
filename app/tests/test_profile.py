import pytest

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from accounts.models import User
from accounts.serializers import UserSerializer
from scripts.seed_db import get_user_data
from tests.conftest import PROFILE_URL


@pytest.mark.django_db
def test_get_profile_without_authorization(anonymous_client):
    client, user = anonymous_client
    response = client.get(path=PROFILE_URL)

    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.parametrize(
    'client_fixture',
    ['authorized_client', 'author_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_profile(client_fixture, request):
    client, user = request.getfixturevalue(client_fixture)
    response = client.get(path=PROFILE_URL)

    assert response.status_code == HTTP_200_OK
    assert response.json() == UserSerializer(user).data


@pytest.mark.parametrize(
    'client_fixture, code',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED),
        ('authorized_client', HTTP_204_NO_CONTENT),
        ('author_client', HTTP_204_NO_CONTENT),
        ('admin_client', HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.django_db
def test_delete_profile(client_fixture, code, request):
    client, user = request.getfixturevalue(client_fixture)
    response = client.delete(path=PROFILE_URL)

    assert response.status_code == code
    assert User.objects.count() == 0

    response = client.get(path=PROFILE_URL)
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    'client_fixture',
    ['authorized_client', 'author_client', 'admin_client'],
)
@pytest.mark.django_db
def test_put_profile(client_fixture, password, request):
    client, user = request.getfixturevalue(client_fixture)
    user_data = get_user_data()
    response = client.put(path=PROFILE_URL, data=user_data, type='json')

    new_password = user_data.pop('password')
    user.refresh_from_db()
    assert response.status_code == HTTP_200_OK
    assert User.objects.get(**user_data) == user
    assert not user.check_password(new_password)
    assert user.check_password(password)


@pytest.mark.parametrize(
    'client_fixture',
    ['authorized_client', 'author_client'],
)
@pytest.mark.django_db
def test_patch_profile_usual_user_to_admin(client_fixture, request):
    client, user = request.getfixturevalue(client_fixture)
    user_data = {'is_staff': True, 'is_superuser': True}
    response = client.patch(path=PROFILE_URL, data=user_data, type='json')

    user.refresh_from_db()
    assert response.status_code == HTTP_200_OK
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.parametrize(
    'client_fixture, code, errors',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
        ('author_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
        ('admin_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
    ],
)
@pytest.mark.django_db
def test_patch_profile_username_with_existing(client_fixture, code, errors, request):
    client, _ = request.getfixturevalue(client_fixture)
    user = User.objects.create_user(**get_user_data())
    response = client.patch(path=PROFILE_URL, data={'username': user.username}, type='json')

    assert response.status_code == code
    assert User.objects.get(username=user.username) == user
    assert response.json().get('username') == errors


@pytest.mark.parametrize(
    'client_fixture, code, errors',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
        ('author_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
        ('admin_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
    ],
)
@pytest.mark.django_db
def test_patch_profile_email_with_existing(client_fixture, code, errors, request):
    client, _ = request.getfixturevalue(client_fixture)
    user = User.objects.create_user(**get_user_data())
    response = client.patch(path=PROFILE_URL, data={'email': user.email}, type='json')

    assert response.status_code == code
    assert User.objects.get(email=user.email) == user
    assert response.json().get('email') == errors
