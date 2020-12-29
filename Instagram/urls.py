from django.contrib import admin
from django.urls import path

from API.auth.auth import get_confirmation_key, login_user, confirm_user

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/account/register/get_confirmation_key',get_confirmation_key),
    path('api/account/register/confirm_user',confirm_user),

    path('api/account/login',login_user),
    
]
