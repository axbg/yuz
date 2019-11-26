from django.urls import path

from . import views

urlpatterns = [
    path('', views.RootEndpoint.as_view(), name='root')
]