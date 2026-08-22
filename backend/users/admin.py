from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "handle", "is_mod", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("The Pond", {"fields": ("handle", "bio", "avatar", "is_mod")}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow)