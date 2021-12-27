import pytest
from random import randint
from urllib.parse import urljoin

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from blog.models import Post
from blog.serializers import PostSerializer
from blog.tests.conftest import fake, POSTS_URL
from scripts.seed_db import get_post_data


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_posts_list(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=POSTS_URL)

    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json().get('results'), list)


@pytest.mark.parametrize(
    'client_fixture, code, count, exists',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, 0, False),
        ('authorized_client', HTTP_201_CREATED, 1, True),
        ('admin_client', HTTP_201_CREATED, 1, True),
    ],
)
@pytest.mark.django_db
def test_post_new_post(client_fixture, code, count, exists, request, category):
    client, user = request.getfixturevalue(client_fixture)
    post_data = get_post_data(category_id=category.id)
    response = client.post(path=POSTS_URL, data=post_data, format='json')

    assert response.status_code == code
    assert Post.objects.count() == count
    created_post = Post.objects.filter(**post_data)
    assert created_post.exists() is exists

    if exists:
        response_data = response.json()
        post = created_post.first()

        assert post.author == user
        assert response_data['author_id'] == user.id
        for key in post_data:
            assert response_data[key] == post_data[key]


@pytest.mark.parametrize(
    'client_fixture, code, error',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
        ('author_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
        ('admin_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
    ],
)
@pytest.mark.django_db
def test_post_new_post_with_existing_title(client_fixture, code, error, request, category, post):
    client, user = request.getfixturevalue(client_fixture)
    post_data = get_post_data(title=post.title, category_id=category.id)
    response = client.post(path=POSTS_URL, data=post_data, format='json')

    assert response.status_code == code
    assert Post.objects.count() == 1
    assert response.json().get('title') == error


@pytest.mark.parametrize(
    'client_fixture, code, errors',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_400_BAD_REQUEST, ['Invalid pk "1" - object does not exist.']),
        ('admin_client', HTTP_400_BAD_REQUEST, ['Invalid pk "1" - object does not exist.']),
    ],
)
@pytest.mark.django_db
def test_post_new_post_with_non_existed_category(client_fixture, code, errors, request):
    client, user = request.getfixturevalue(client_fixture)
    post_data = get_post_data(category_id=1)
    response = client.post(path=POSTS_URL, data=post_data, format='json')

    assert response.status_code == code
    assert Post.objects.count() == 0
    assert response.json().get('category_id') == errors


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'author_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_existing_post_details(client_fixture, request, post):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=urljoin(POSTS_URL, f'{post.pk}/'))

    assert response.status_code == HTTP_200_OK
    expected_data = PostSerializer(post).data
    expected_data['updated_at'] = str(expected_data['updated_at'])
    expected_data['created_at'] = str(expected_data['created_at'])
    assert response.json() == expected_data


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'author_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_non_existing_post_details(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=urljoin(POSTS_URL, f'{randint(1, 10)}/'))

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    'client_fixture, code, count',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, 1),
        ('authorized_client', HTTP_403_FORBIDDEN, 1),
        ('author_client', HTTP_204_NO_CONTENT, 0),
        ('admin_client', HTTP_204_NO_CONTENT, 0),
    ],
)
@pytest.mark.django_db
def test_delete_existing_post(client_fixture, code, count, request, post):
    client, user = request.getfixturevalue(client_fixture)
    response = client.delete(path=urljoin(POSTS_URL, f'{post.pk}/'))

    assert response.status_code == code
    assert Post.objects.count() == count


@pytest.mark.parametrize(
    'client_fixture, code',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED),
        ('authorized_client', HTTP_404_NOT_FOUND),
        ('author_client', HTTP_404_NOT_FOUND),
        ('admin_client', HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.django_db
def test_delete_non_existent_post(client_fixture, code, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.delete(path=urljoin(POSTS_URL, f'{randint(1, 10)}/'))

    assert response.status_code == code


@pytest.mark.parametrize(
    'client_fixture, code, exists',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, False),
        ('authorized_client', HTTP_403_FORBIDDEN, False),
        ('author_client', HTTP_200_OK, True),
        ('admin_client', HTTP_200_OK, True),
    ],
)
@pytest.mark.django_db
def test_put_existing_post(client_fixture, code, exists, request, post, author):
    client, _ = request.getfixturevalue(client_fixture)
    post_data = get_post_data(author_id=post.author.id)
    response = client.put(path=urljoin(POSTS_URL, f'{post.pk}/'), data=post_data, format='json')

    assert response.status_code == code
    assert Post.objects.count() == 1
    created_post = Post.objects.filter(**post_data)
    assert created_post.exists() is exists

    if exists:
        response_data = response.json()
        post = created_post.first()

        assert post.author == author
        assert response_data['author_id'] == author.id
        for key in post_data:
            assert response_data[key] == post_data[key]


@pytest.mark.parametrize(
    'client_fixture, code, exists',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, False),
        ('authorized_client', HTTP_404_NOT_FOUND, False),
        ('author_client', HTTP_404_NOT_FOUND, True),
        ('admin_client', HTTP_404_NOT_FOUND, True),
    ],
)
@pytest.mark.django_db
def test_put_non_existent_post(client_fixture, code, exists, request):
    client, user = request.getfixturevalue(client_fixture)
    post_data = get_post_data()
    response = client.put(path=urljoin(POSTS_URL, f'{randint(1, 10)}/'), data=post_data, format='json')

    assert response.status_code == code
    assert Post.objects.count() == 0


@pytest.mark.parametrize(
    'client_fixture, code, error',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_403_FORBIDDEN, None),
        ('author_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
        ('admin_client', HTTP_400_BAD_REQUEST, ['This field must be unique.']),
    ],
)
@pytest.mark.django_db
def test_put_post_with_existing_title(client_fixture, code, error, request, post):
    client, user = request.getfixturevalue(client_fixture)
    post_data = get_post_data(author_id=post.author.id)
    other_post = Post.objects.create(**post_data)

    post_data['title'] = post.title
    response = client.put(path=urljoin(POSTS_URL, f'{other_post.pk}/'), data=post_data, format='json')

    assert response.status_code == code
    assert Post.objects.count() == 2
    assert Post.objects.get(title=post.title) == post
    assert response.json().get('title') == error


@pytest.mark.parametrize(
    'client_fixture, code, error',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_403_FORBIDDEN, None),
        ('author_client', HTTP_400_BAD_REQUEST, ['Invalid pk "2" - object does not exist.']),
        ('admin_client', HTTP_400_BAD_REQUEST, ['Invalid pk "2" - object does not exist.']),
    ],
)
@pytest.mark.django_db
def test_put_post_with_non_existent_category(client_fixture, code, error, request, post):
    client, user = request.getfixturevalue(client_fixture)
    post_data = get_post_data(category_id=2)
    response = client.put(path=urljoin(POSTS_URL, f'{post.pk}/'), data=post_data, format='json')

    assert response.status_code == code
    assert response.json().get('category_id') == error
