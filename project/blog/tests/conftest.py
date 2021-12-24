import pytest
from faker import Faker

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from blog.models import Category
from scripts.seed_db import get_category_data


fake = Faker()
TOKEN_URL = reverse('tokens')
CATEGORIES_URL = reverse('categories-list')
POSTS_URL = reverse('posts-list')
COMMENTS_URL = reverse('comments-list')


@pytest.fixture
def anonymous_client():
    client = APIClient()
    return client


@pytest.fixture
def authorized_client(anonymous_client):
    User.objects.create_user(username='test', password='test')
    access_token = anonymous_client.post(
        TOKEN_URL, data={'username': 'test', 'password': 'test'}
    ).json()['access']
    anonymous_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return anonymous_client


@pytest.fixture
def admin_client(anonymous_client):
    User.objects.create_superuser(username='test', password='test')
    access_token = anonymous_client.post(
        TOKEN_URL, data={'username': 'test', 'password': 'test'}
    ).json()['access']
    anonymous_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return anonymous_client


@pytest.fixture
def category():
    category = Category.objects.create(
        **get_category_data()
    )
    return category
