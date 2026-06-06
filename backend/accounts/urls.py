from django.urls import path
from .views import me, register

urlpatterns = [
    path('me/',       me,       name='auth_me'),
    path('register/', register, name='auth_register'),
]
