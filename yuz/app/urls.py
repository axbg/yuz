from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('connection/', views.RootView.as_view(), name='root'),
    
    # REST Interface
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('extract/', views.ExtractorEndpoint.as_view(), name='extractor'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    #Web app
    path('', views.WebView.as_view(get_template="index.html", post_template="result.html"))
]