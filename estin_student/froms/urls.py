from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('',              views.resource_list,    name='resource_list'),
    path('upload/',       views.upload_resource,  name='upload'),
    path('<int:pk>/download/', views.download_resource, name='download'),

    # AJAX
    path('ajax/modules/', views.ajax_get_modules, name='ajax_modules'),
]
