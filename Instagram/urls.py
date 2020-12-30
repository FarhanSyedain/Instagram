from django.contrib import admin
from django.urls import path

from API.auth.auth import get_confirmation_key, login_user, confirm_user, request_password_reset, reset_password

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/account/register/get_confirmation_key',get_confirmation_key),
    path('api/account/register/confirm_user',confirm_user),
    path('api/account/password/forgot/get_confirmation',request_password_reset),
    path('api/account/password/forgot/reset',reset_password),

    path('api/account/login',login_user),
    
]
