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

from blog.models import Comment
from blog.serializers import CommentSerializer
from scripts.seed_db import get_comment_data
from tests.conftest import fake, COMMENTS_URL


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_comments_list(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=COMMENTS_URL)

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
def test_post_new_comment(client_fixture, code, count, exists, request, post):
    client, user = request.getfixturevalue(client_fixture)
    comment_data = get_comment_data(post_id=post.id)
    comment_data.pop('author_id')
    response = client.post(path=COMMENTS_URL, data=comment_data, format='json')
    assert response.status_code == code
    assert Comment.objects.count() == count
    created_comment = Comment.objects.filter(**comment_data)
    assert created_comment.exists() is exists

    if exists:
        response_data = response.json()
        comment = created_comment.first()

        assert comment.author == user
        assert response_data['author_id'] == user.id
        for key in comment_data:
            assert response_data[key] == comment_data[key]


@pytest.mark.parametrize(
    'client_fixture, code, errors',
    [
        ('anonymous_client', HTTP_401_UNAUTHORIZED, None),
        ('authorized_client', HTTP_400_BAD_REQUEST, ['Invalid pk "1" - object does not exist.']),
        ('admin_client', HTTP_400_BAD_REQUEST, ['Invalid pk "1" - object does not exist.']),
    ],
)
@pytest.mark.django_db
def test_post_new_comment_for_non_existed_post(client_fixture, code, errors, request):
    client, _ = request.getfixturevalue(client_fixture)
    comment_data = get_comment_data(post_id=1)
    response = client.post(path=COMMENTS_URL, data=comment_data, format='json')

    assert response.status_code == code
    assert Comment.objects.count() == 0
    assert response.json().get('post_id') == errors


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'author_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_existing_comment_details(client_fixture, request, comment):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=urljoin(COMMENTS_URL, f'{comment.pk}/'))

    assert response.status_code == HTTP_200_OK
    expected_data = CommentSerializer(comment).data
    expected_data['updated_at'] = str(expected_data['updated_at'])
    expected_data['created_at'] = str(expected_data['created_at'])
    assert response.json() == expected_data


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'author_client', 'admin_client'],
)
@pytest.mark.django_db
def test_get_non_existing_comment_details(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path=urljoin(COMMENTS_URL, f'{randint(1, 10)}/'))

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
def test_delete_existing_comment(client_fixture, code, count, request, comment):
    client, user = request.getfixturevalue(client_fixture)
    response = client.delete(path=urljoin(COMMENTS_URL, f'{comment.pk}/'))

    assert response.status_code == code
    assert Comment.objects.count() == count


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
def test_delete_non_existent_comment(client_fixture, code, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.delete(path=urljoin(COMMENTS_URL, f'{randint(1, 10)}/'))

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
def test_put_existing_post(client_fixture, code, exists, request, comment, author):
    client, _ = request.getfixturevalue(client_fixture)
    comment_data = get_comment_data(author_id=comment.author.id)
    comment_data.pop('author_id')
    response = client.put(path=urljoin(COMMENTS_URL, f'{comment.pk}/'), data=comment_data, format='json')

    assert response.status_code == code
    assert Comment.objects.count() == 1
    created_post = Comment.objects.filter(**comment_data)
    assert created_post.exists() is exists

    if exists:
        response_data = response.json()
        comment = created_post.first()

        assert comment.author == author
        assert response_data['author_id'] == author.id
        for key in comment_data:
            assert response_data[key] == comment_data[key]


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
def test_put_non_existent_comment(client_fixture, code, exists, request):
    client, user = request.getfixturevalue(client_fixture)
    post_data = get_comment_data()
    response = client.put(path=urljoin(COMMENTS_URL, f'{randint(1, 10)}/'), data=post_data, format='json')

    assert response.status_code == code
    assert Comment.objects.count() == 0


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
def test_put_comment_for_non_existent_post(client_fixture, code, error, request, comment):
    client, user = request.getfixturevalue(client_fixture)
    comment_data = get_comment_data(post_id=2)
    response = client.put(path=urljoin(COMMENTS_URL, f'{comment.pk}/'), data=comment_data, format='json')

    assert response.status_code == code
    assert response.json().get('post_id') == error
