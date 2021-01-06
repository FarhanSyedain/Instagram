from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from API.auth.auth import get_confirmation_key, login_user, confirm_user, request_password_reset, reset_password, resend_confirmation_key
from API.profile import  update_user, delete_user



urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/account/register/get_confirmation_key',get_confirmation_key),
    path('api/account/register/confirm_user',confirm_user),
    path('api/account/password/forgot/get_confirmation',request_password_reset),
    path('api/account/password/forgot/reset',reset_password),
    path('api/account/obtain_token',login_user),

    path('api/account/user/update',update_user),
    path('api/account/user/delete',delete_user),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    