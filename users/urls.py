from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    #RegisterView,
    ProfileView,
    MyClassesListView,
    MyProjectsListView,
    NotificationsListView,
    JoinClassView,
    )

urlpatterns = [
    #path('register/',RegisterView,name='users-register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/users-login.html'),name='users-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/users-logout.html'),name='users-logout'),
    path('my-classes/',MyClassesListView,name='users-my-classes'),
    path('my-projects/',MyProjectsListView,name='users-my-projects'),
    path('my-profile/',ProfileView,name='users-my-profile'),
    path('my-notifications/',NotificationsListView,name='users-my-notifications'),
    path('join-class/',JoinClassView,name='users-join-class'),
]