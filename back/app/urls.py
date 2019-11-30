from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.RootView.as_view(), name='root'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('extract/', views.ExtractorEndpoint.as_view(), name='extractor'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]