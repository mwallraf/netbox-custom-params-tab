from netbox.api.routers import NetBoxRouter
from . import views

router = NetBoxRouter()
router.register('custom-tab-configs', views.CustomTabConfigViewSet)

urlpatterns = router.urls
