import pytest

from rest_framework.status import HTTP_201_CREATED
from blog.tests.conftest import SIGNUP_URL
from django.contrib.auth.models import User
from scripts.seed_db import get_user_data


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'admin_client'],
)
@pytest.mark.django_db
def test_put_category_with_existing_name(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    user_data = get_user_data()
    user_count = User.objects.count()
    response = client.post(path=SIGNUP_URL, data=user_data, format='json')

    password = user_data.pop('password')
    assert response.status_code == HTTP_201_CREATED
    assert User.objects.count() == user_count + 1
    user = User.objects.get(**user_data)
    assert user
    assert user.check_password(password)
