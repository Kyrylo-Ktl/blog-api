from typing import Dict

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

TOKEN_URL = reverse('tokens')


def authorize_client(client: APIClient, data: Dict) -> None:
    access_token = client.post(
        TOKEN_URL,
        data=data,
    ).json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
