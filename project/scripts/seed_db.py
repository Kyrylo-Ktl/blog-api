"""Module with functions for filling the database with random data"""

import secrets

from blog.models import Category, Comment, Post
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()


def get_category_data(**kwargs):
    return {
        'name': kwargs.get('name', f'{fake.word().capitalize()} {fake.word()}'),
    }


def get_user_data(**kwargs):
    return {
        'email': kwargs.get('email', fake.email()),
        'username': kwargs.get('username', fake.word()),
        'first_name': kwargs.get('first_name', fake.first_name()),
        'last_name': kwargs.get('last_name', fake.last_name()),
        'password': kwargs.get('password', secrets.token_hex(nbytes=16)),
    }


def get_post_data(**kwargs):
    random_user = get_user_model().objects.order_by('?').first()
    random_category = Category.objects.order_by('?').first()
    return {
        'title': kwargs.get('title', fake.text(100)),
        'text': kwargs.get('text', fake.text(1000)),
        'author_id': kwargs.get('author_id', random_user.id if random_user else None),
        'category_id': kwargs.get('category_id', random_category.id if random_category else None),
    }


def get_comment_data(**kwargs):
    random_user = get_user_model().objects.order_by('?').first()
    random_post = Post.objects.order_by('?').first()
    return {
        'text': kwargs.get('text', fake.text(500)),
        'author_id': kwargs.get('author_id', random_user.id if random_user else None),
        'post_id': kwargs.get('post_id', random_post.id if random_post else None),
    }


def create_n_instances(model, n_instances, data_function):
    model.objects.bulk_create([
        model(**data_function())
        for _ in range(n_instances)
    ])


def seed_categories(n_categories: int = 10):
    create_n_instances(Category, n_categories, get_category_data)


def seed_users(n_users: int = 10):
    create_n_instances(get_user_model(), n_users, get_user_data)


def seed_posts(n_posts: int = 10):
    create_n_instances(Post, n_posts, get_post_data)


def seed_comments(n_comments: int = 10):
    create_n_instances(Comment, n_comments, get_comment_data)


def run():
    seed_categories(10)
    seed_users(10)
    seed_posts(20)
    seed_comments(100)
