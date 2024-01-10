from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('dashboard', views.dashboard_view, name="dashboard"),
    path('profile', views.profile_view, name="profile"),
    path('logout', views.logout_view, name='logout'),
]