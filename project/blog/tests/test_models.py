import pytest

from blog.models import Category, Comment, Post
from django.core.exceptions import ValidationError
from scripts.seed_db import get_post_data, get_comment_data, get_category_data


def helper_test_create_model_with_invalid_data(invalid_data, model, error):
    with pytest.raises(ValidationError) as excinfo:
        model(**invalid_data).save()
    assert str(excinfo.value) == error
    assert model.objects.count() == 0


@pytest.mark.parametrize(
    'invalid_value, field, error',
    [
        ('_'*2, 'name', 'Ensure this value has at least 4 characters (it has 2).'),
        ('_'*150, 'name', 'Ensure this value has at most 128 characters (it has 150).'),
    ]
)
@pytest.mark.django_db
def test_create_category_with_invalid_data(invalid_value, field, error):
    category_data = get_category_data(**{field: invalid_value})
    helper_test_create_model_with_invalid_data(
        invalid_data=category_data,
        model=Category,
        error=str({field: [error]}),
    )


@pytest.mark.parametrize(
    'invalid_value, field, error',
    [
        ('_'*10, 'title', 'Ensure this value has at least 16 characters (it has 10).'),
        ('_'*150, 'title', 'Ensure this value has at most 128 characters (it has 150).'),
        ('_'*100, 'text', 'Ensure this value has at least 128 characters (it has 100).'),
        ('_'*1050, 'text', 'Ensure this value has at most 1024 characters (it has 1050).'),
    ]
)
@pytest.mark.django_db
def test_create_post_with_invalid_data(invalid_value, field, error, author, category):
    post_data = get_post_data(**{field: invalid_value})
    helper_test_create_model_with_invalid_data(
        invalid_data=post_data,
        model=Post,
        error=str({field: [error]}),
    )


@pytest.mark.parametrize(
    'invalid_value, field, error',
    [
        ('_'*6, 'text', 'Ensure this value has at least 8 characters (it has 6).'),
        ('_'*525, 'text', 'Ensure this value has at most 512 characters (it has 525).'),
    ]
)
@pytest.mark.django_db
def test_create_comment_with_invalid_data(invalid_value, field, error, author, post):
    comment_data = get_comment_data(**{field: invalid_value})
    helper_test_create_model_with_invalid_data(
        invalid_data=comment_data,
        model=Comment,
        error=str({field: [error]}),
    )
