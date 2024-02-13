from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UsersAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )


admin.site.unregister(User)
admin.site.register(User, UsersAdmin)
