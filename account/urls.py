from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view  
app_name = 'account'

urlpatterns = [
     path('register/', views.signup, name='signup'),
     path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
      path('logout/', logout_view, name='logout')
]