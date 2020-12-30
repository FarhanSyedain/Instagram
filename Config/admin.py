from django.contrib import admin
from .models import ConfirmationKey, PasswordResetKey
# Register your models here.

admin.site.register(ConfirmationKey)
admin.site.register(PasswordResetKey)
