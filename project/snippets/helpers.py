"""Module with helper functions"""

from django.conf import settings
from django.urls import reverse


def reverse_external(url: str, **kwargs) -> str:
    domain = f'http://{settings.APP_HOST}:{settings.APP_PORT}'
    full_url = domain + reverse(url, kwargs=kwargs)
    return full_url
