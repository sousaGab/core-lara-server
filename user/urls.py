from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_view),
    path('login/', views.login_view),
]
