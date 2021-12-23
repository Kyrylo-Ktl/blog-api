"""Module with functions for filling the database with random data"""

from blog.models import Category, Comment, Post
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()


def seed_categories(n_categories: int = 10):
    Category.objects.bulk_create([
        Category(name=fake.word())
        for _ in range(n_categories)
    ])


def seed_users(n_users: int = 10):
    get_user_model().objects.bulk_create([
        get_user_model()(
            email=fake.email(),
            username=fake.first_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password='testing123',
        )
        for _ in range(n_users)
    ])


def seed_posts(n_posts: int = 10):
    Post.objects.bulk_create([
        Post(
            title=fake.text(100),
            text=fake.text(1000),
            author=get_user_model().objects.order_by('?').first(),
            category=Category.objects.order_by('?').first(),
        )
        for _ in range(n_posts)
    ])


def seed_comments(n_comments: int = 10):
    Comment.objects.bulk_create([
        Comment(
            text=fake.text(500),
            author=get_user_model().objects.order_by('?').first(),
            post=Post.objects.order_by('?').first(),
        )
        for _ in range(n_comments)
    ])


def run():
    seed_categories(10)
    seed_users(10)
    seed_posts(20)
    seed_comments(100)
