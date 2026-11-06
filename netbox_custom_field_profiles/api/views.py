from netbox.api.viewsets import NetBoxModelViewSet
from ..models import CustomTabConfig
from .serializers import CustomTabConfigSerializer


class CustomTabConfigViewSet(NetBoxModelViewSet):
    queryset = CustomTabConfig.objects.prefetch_related('config_groups', 'config_fields')
    serializer_class = CustomTabConfigSerializer
