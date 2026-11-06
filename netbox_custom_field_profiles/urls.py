from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomTabConfigListView.as_view(), name='customtabconfig_list'),
    path('add/', views.CustomTabConfigEditView.as_view(), name='customtabconfig_add'),
    path('<int:pk>/', views.CustomTabConfigView.as_view(), name='customtabconfig'),
    path('<int:pk>/edit/', views.CustomTabConfigEditView.as_view(), name='customtabconfig_edit'),
    path('<int:pk>/delete/', views.CustomTabConfigDeleteView.as_view(), name='customtabconfig_delete'),
]
