from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

import users.models


class ProfileInline(admin.StackedInline):
    model = users.models.Profile
    can_delete = False
    verbose_name_plural = "Профили"
    readonly_fields = (users.models.Profile.coffee_count.field.name,)


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


__all__ = ()
