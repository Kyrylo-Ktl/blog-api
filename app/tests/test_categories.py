from random import randint
from urllib.parse import urljoin

import pytest

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from tests.conftest import CATEGORIES_URL, fake
from scripts.seed_db import get_category_data
from blog.models import Category
from blog.serializers import CategorySerializer


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_category_list(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=CATEGORIES_URL)

    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json().get('results'), list)


@pytest.mark.parametrize(
    'client_fixture, code, count, exists',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, 0, False),
        ('authorized_client', HTTP_403_FORBIDDEN, 0, False),
        ('admin_client', HTTP_201_CREATED, 1, True),
    ],
)
@pytest.mark.django_db
def test_post_category(client_fixture, code, count, exists, request):
    client, _ = request.getfixturevalue(client_fixture)
    category_data = get_category_data()
    response = client.post(path=CATEGORIES_URL, data=category_data, format='json')

    assert response.status_code == code
    assert Category.objects.count() == count
    assert Category.objects.filter(**category_data).exists() == exists


@pytest.mark.parametrize(
    'client_fixture, code, error',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_403_FORBIDDEN, None),
        ('admin_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
    ],
)
@pytest.mark.django_db
def test_post_category_with_existing_name(client_fixture, code, error, request, category):
    client, _ = request.getfixturevalue(client_fixture)
    category_data = get_category_data(name=category.name)
    response = client.post(path=CATEGORIES_URL, data=category_data, format='json')

    assert response.status_code == code
    assert Category.objects.count() == 1
    assert response.json().get('name') == error


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_existing_category_details(client_fixture, request, category):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=urljoin(CATEGORIES_URL, f'{category.pk}/'))

    assert response.status_code == HTTP_200_OK
    assert response.json() == CategorySerializer(category).data


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_non_existing_category_details(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=urljoin(CATEGORIES_URL, f'{randint(1, 100)}/'))

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    'client_fixture, code, count',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, 1),
        ('authorized_client', HTTP_403_FORBIDDEN, 1),
        ('admin_client', HTTP_204_NO_CONTENT, 0),
    ],
)
@pytest.mark.django_db
def test_delete_existing_category(client_fixture, code, count, request, category):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.delete(path=urljoin(CATEGORIES_URL, f'{category.pk}/'))

    assert response.status_code == code
    assert Category.objects.count() == count


@pytest.mark.parametrize(
    'client_fixture, code',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED),
        ('authorized_client', HTTP_403_FORBIDDEN),
        ('admin_client', HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.django_db
def test_delete_non_existing_category(client_fixture, code, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.delete(path=urljoin(CATEGORIES_URL, f'{randint(1, 100)}/'))

    assert response.status_code == code


@pytest.mark.parametrize(
    'client_fixture, code, exists',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, False),
        ('authorized_client', HTTP_403_FORBIDDEN, False),
        ('admin_client', HTTP_200_OK, True),
    ],
)
@pytest.mark.django_db
def test_put_existing_category(client_fixture, code, exists, request, category):
    client, _ = request.getfixturevalue(client_fixture)
    category_data = get_category_data()
    response = client.put(path=urljoin(CATEGORIES_URL, f'{category.pk}/'), data=category_data, format='json')

    assert response.status_code == code
    assert Category.objects.count() == 1
    assert Category.objects.filter(**category_data).exists() == exists


@pytest.mark.parametrize(
    'client_fixture, code',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED),
        ('authorized_client', HTTP_403_FORBIDDEN),
        ('admin_client', HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.django_db
def test_put_non_existing_category(client_fixture, code, request):
    client, _ = request.getfixturevalue(client_fixture)
    category_data = get_category_data(name=fake.word())
    response = client.put(path=urljoin(CATEGORIES_URL, f'{randint(1, 100)}/'), data=category_data, format='json')

    assert response.status_code == code
    assert Category.objects.count() == 0


@pytest.mark.parametrize(
    'client_fixture, code, error',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_403_FORBIDDEN, None),
        ('admin_client', HTTP_400_BAD_REQUEST, ["This field must be unique."]),
    ],
)
@pytest.mark.django_db
def test_put_category_with_existing_name(client_fixture, code, error, request, category):
    client, _ = request.getfixturevalue(client_fixture)
    category_data = get_category_data()
    other_category = Category.objects.create(**category_data)

    category_data['name'] = category.name
    response = client.put(path=urljoin(CATEGORIES_URL, f'{other_category.pk}/'), data=category_data, format='json')

    assert response.status_code == code
    assert Category.objects.count() == 2
    assert Category.objects.get(**category_data) == category
    assert response.json().get('name') == error
