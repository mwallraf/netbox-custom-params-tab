from netbox.api.serializers import NetBoxModelSerializer
from ..models import CustomFieldProfile


class CustomFieldProfileSerializer(NetBoxModelSerializer):
    """Native event payload; profile management has no public REST endpoint."""

    class Meta:
        model = CustomFieldProfile
        fields = ('id', 'display', 'title', 'content_type', 'display_order', 'enabled',
                  'field_mode', 'created', 'last_updated')
        read_only_fields = fields
