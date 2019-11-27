from django.urls import path

from . import views

urlpatterns = [
    path('', views.RootEndpoint.as_view(), name='root'),
    path('extract', views.ExtractorEndpoint.as_view(), name='extractor')
]