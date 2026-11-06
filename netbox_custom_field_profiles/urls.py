from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomFieldProfileListView.as_view(), name='customfieldprofile_list'),
    path('add/', views.CustomFieldProfileEditView.as_view(), name='customfieldprofile_add'),
    path('<int:pk>/', views.CustomFieldProfileView.as_view(), name='customfieldprofile'),
    path('<int:pk>/edit/', views.CustomFieldProfileEditView.as_view(), name='customfieldprofile_edit'),
    path('<int:pk>/delete/', views.CustomFieldProfileDeleteView.as_view(), name='customfieldprofile_delete'),
]
