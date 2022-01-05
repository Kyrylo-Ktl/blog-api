import pytest

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from accounts.models import User
from scripts.seed_db import get_user_data
from tests.conftest import SIGNUP_URL


@pytest.mark.django_db
def test_signup(anonymous_client):
    client, _ = anonymous_client
    user_data = get_user_data()
    response = client.post(path=SIGNUP_URL, data=user_data, format='json')

    password = user_data.pop('password')
    assert response.status_code == HTTP_201_CREATED
    assert User.objects.count() == 1
    user = User.objects.get(**user_data)
    assert user
    assert user.check_password(password)


@pytest.mark.parametrize(
    'field_to_exclude',
    ['username', 'email', 'password', 'first_name', 'last_name'],
)
@pytest.mark.django_db
def test_signup_without_field(field_to_exclude, anonymous_client):
    client, _ = anonymous_client
    user_data = get_user_data()
    user_data.pop(field_to_exclude)
    response = client.post(path=SIGNUP_URL, data=user_data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert response.json() == {field_to_exclude: ['This field is required.']}
