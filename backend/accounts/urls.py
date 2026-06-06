from django.urls import path
from .views import me, register, reset_password

urlpatterns = [
    path('me/',              me,              name='auth_me'),
    path('register/',        register,        name='auth_register'),
    path('reset-password/',  reset_password,  name='auth_reset_password'),
]
