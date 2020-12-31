from django.contrib import admin
from .models import ConfirmationKey, PasswordResetKey,Profile
# Register your models here.

admin.site.register(ConfirmationKey)
admin.site.register(PasswordResetKey)
admin.site.register(Profile)
