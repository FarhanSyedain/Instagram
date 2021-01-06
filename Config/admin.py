from django.contrib import admin
from .models import ConfirmationKey, PasswordResetKey,Profile, Follow,Following, Post, Posts
# Register your models here.

admin.site.register(ConfirmationKey)
admin.site.register(PasswordResetKey)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Posts)

