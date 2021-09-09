from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
	path('allusers/<str:user>', views.all_user, name = 'alluser'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('dashboard/<str:user>', views.dashboard, name = 'dashboard'),
    path('user/<str:user>', views.user, name = 'user'),
    path('new_post/<str:user>', views.new_post, name = 'newpost')
]