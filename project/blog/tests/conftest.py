import pytest
from faker import Faker

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from accounts.models import User
from blog.models import Category, Comment, Post
from blog.tests.helpers import authorize_client
from scripts.seed_db import (
    get_category_data,
    get_comment_data,
    get_post_data,
    get_random_password,
    get_user_data,
)

fake = Faker()

CATEGORIES_URL = reverse('categories-list')
POSTS_URL = reverse('posts-list')
COMMENTS_URL = reverse('comments-list')

PROFILE_URL = reverse('profile')
SIGNUP_URL = reverse('signup')

PASSWORD_RESET_REQUEST_URL = reverse('request-reset')


@pytest.fixture
def password():
    return get_random_password()


@pytest.fixture
def user(password):
    user_data = get_user_data(password=password)
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def author(password):
    user_data = get_user_data(password=password)
    admin = User.objects.create_user(**user_data)
    return admin


@pytest.fixture
def admin(password):
    user_data = get_user_data(password=password)
    admin = User.objects.create_superuser(**user_data)
    return admin


@pytest.fixture
def anonymous_client():
    client = APIClient()
    return client, None


@pytest.fixture
def authorized_client(anonymous_client, user, password):
    client, _ = anonymous_client
    authorize_client(client, {'username': user.username, 'password': password})
    return client, user


@pytest.fixture
def author_client(anonymous_client, author, password):
    client, _ = anonymous_client
    authorize_client(client, {'username': author.username, 'password': password})
    return client, author


@pytest.fixture
def admin_client(anonymous_client, admin, password):
    client, _ = anonymous_client
    authorize_client(client, {'username': admin.username, 'password': password})
    return client, admin


@pytest.fixture
def category():
    category = Category.objects.create(
        **get_category_data()
    )
    return category


@pytest.fixture
def post(category, author):
    post = Post.objects.create(
        **get_post_data()
    )
    return post


@pytest.fixture
def comment(post, author):
    comment = Comment.objects.create(
        **get_comment_data()
    )
    return comment
