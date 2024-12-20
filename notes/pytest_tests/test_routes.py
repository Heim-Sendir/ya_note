from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse


@pytest.mark.parametrize('name', (
    'notes:home',
    'users:login',
    'users:signup',
    'users:logout'
))
def test_home_availability_for_anoymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('name', (
    'notes:list',
    'notes:success',
    'notes:add'
))
def test_page_availability_for_authorized_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND)
    )
)
@pytest.mark.parametrize('name', (
    'notes:detail',
    'notes:edit',
    'notes:delete'
))
def test_pages_availability_for_author(
    parametrized_client, name, note, expected_status
):
    url = reverse(name, args=(note.slug,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', pytest.lazy_fixture('slug_for_agrs')),
        ('notes:edit', pytest.lazy_fixture('slug_for_agrs')),
        ('notes:delete', pytest.lazy_fixture('slug_for_agrs')),
        ('notes:add', None),
        ('notes:list', None),
        ('notes:success', None),
    )
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    excepted_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, excepted_url)
