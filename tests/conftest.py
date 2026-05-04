import pytest
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        password='password',
        email='admin@example.com',
    )


@pytest.fixture
def client_logged_in(client, admin_user):
    client.force_login(admin_user)
    return client


@pytest.fixture
def device_content_type(db):
    return ContentType.objects.get(app_label='dcim', model='device')


@pytest.fixture
def site_content_type(db):
    return ContentType.objects.get(app_label='dcim', model='site')
