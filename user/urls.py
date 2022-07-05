from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_view, name='user'),
    path('login/', views.login_view, name='login'),
]
