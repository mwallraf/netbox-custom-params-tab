from netbox.api.serializers import NetBoxModelSerializer
from ..models import CustomTabConfig


class CustomTabConfigSerializer(NetBoxModelSerializer):
    class Meta:
        model = CustomTabConfig
        fields = ('id', 'url', 'display', 'content_type', 'tab_label', 'enabled', 'created', 'last_updated')
        brief_fields = ('id', 'url', 'display', 'tab_label')
