import pytest
from django.urls import reverse
from netbox_custom_field_profiles.models import CustomTabConfig
from netbox_custom_field_profiles.forms import GROUP_FORMSET_PREFIX, FIELD_FORMSET_PREFIX


def _empty_formset_data(prefix):
    return {
        f'{prefix}-TOTAL_FORMS': '0',
        f'{prefix}-INITIAL_FORMS': '0',
        f'{prefix}-MIN_NUM_FORMS': '0',
        f'{prefix}-MAX_NUM_FORMS': '1000',
    }


@pytest.mark.django_db
class TestCustomTabConfigListView:
    def test_returns_200(self, client_logged_in):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_list')
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_list')
        response = client.get(url)
        assert response.status_code in (302, 403)


@pytest.mark.django_db
class TestCustomTabConfigEditView:
    def test_get_add_returns_200(self, client_logged_in):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_add')
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_unauthenticated_add_redirects(self, client):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_add')
        response = client.get(url)
        assert response.status_code in (302, 403)

    def test_unauthenticated_edit_redirects(self, client, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_edit', args=[config.pk])
        response = client.get(url)
        assert response.status_code in (302, 403)

    def test_post_creates_config(self, client_logged_in, device_content_type):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_add')
        data = {
            'content_type': device_content_type.pk,
            'tab_label': 'Parameters',
            'enabled': True,
            **_empty_formset_data(GROUP_FORMSET_PREFIX),
            **_empty_formset_data(FIELD_FORMSET_PREFIX),
        }
        response = client_logged_in.post(url, data)
        assert response.status_code == 302
        assert CustomTabConfig.objects.filter(content_type=device_content_type).exists()

    def test_get_edit_returns_200(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_edit', args=[config.pk])
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_edit_updates_tab_label(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type, tab_label='Old Label'
        )
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_edit', args=[config.pk])
        data = {
            'content_type': device_content_type.pk,
            'tab_label': 'New Label',
            'enabled': True,
            **_empty_formset_data(GROUP_FORMSET_PREFIX),
            **_empty_formset_data(FIELD_FORMSET_PREFIX),
        }
        response = client_logged_in.post(url, data)
        assert response.status_code == 302
        config.refresh_from_db()
        assert config.tab_label == 'New Label'


@pytest.mark.django_db
class TestCustomTabConfigDeleteView:
    def test_get_delete_returns_200(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_delete', args=[config.pk])
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_post_delete_removes_config(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_delete', args=[config.pk])
        response = client_logged_in.post(url, {'confirm': True})
        assert response.status_code in (200, 302)
        assert not CustomTabConfig.objects.filter(pk=config.pk).exists()
