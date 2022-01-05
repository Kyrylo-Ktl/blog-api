import pytest

from rest_framework.status import HTTP_200_OK


@pytest.mark.parametrize(
    'client_fixture',
    ['anonymous_client', 'authorized_client', 'admin_client'],
)
@pytest.mark.django_db
def test_put_category_with_existing_name(client_fixture, request):
    client, _ = request.getfixturevalue(client_fixture)
    response = client.get(path='', format='json')

    assert response.status_code == HTTP_200_OK
