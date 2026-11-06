from netbox.api.serializers import NetBoxModelSerializer
from ..models import CustomFieldProfile, CustomTabConfig


class CustomFieldProfileSerializer(NetBoxModelSerializer):
    """Native event payload; profile management has no public REST endpoint."""

    class Meta:
        model = CustomFieldProfile
        fields = ('id', 'display', 'title', 'content_type', 'display_order', 'enabled',
                  'field_mode', 'created', 'last_updated')
        read_only_fields = fields


class CustomTabConfigSerializer(NetBoxModelSerializer):
    class Meta:
        model = CustomTabConfig
        fields = ('id', 'url', 'display', 'content_type', 'tab_label', 'enabled', 'created', 'last_updated')
        brief_fields = ('id', 'url', 'display', 'tab_label')
