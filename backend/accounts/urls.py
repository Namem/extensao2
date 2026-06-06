from django.urls import path
from .views import me, register, forgot_password, reset_password

urlpatterns = [
    path('me/',              me,              name='auth_me'),
    path('register/',        register,        name='auth_register'),
    path('forgot-password/', forgot_password, name='auth_forgot_password'),
    path('reset-password/',  reset_password,  name='auth_reset_password'),
]
