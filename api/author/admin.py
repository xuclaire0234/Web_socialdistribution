# 2023-02-13
# author/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AuthorCreationForm, AuthorChangeForm
from .models import Author
# This code is modified from an article from Michael Herman on 2023-01-22 retrieved on 2023-02-15, to testdriven.io
# article here:
# https://testdriven.io/blog/django-custom-user-model/#forms
class AuthorAdmin(UserAdmin):
    add_form = AuthorCreationForm
    form = AuthorChangeForm
    model = Author
    list_display = ('id', 'username', 'host', 'display_name', 'github', 'profile_image', 'is_staff', 'is_active')
    list_filter = ('id', 'username', 'host', 'display_name', 'github', 'profile_image', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'host')}),
        ('Permissions', {'fields': ("is_staff", "is_active", "groups", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'id', 'username', 'host',
                'password1', 'password2', 
                'is_staff', 'is_active', 'groups', 'user_permissions'
            )}
        ),
    )
    search_fields = ('id', 'username', 'host')
    ordering = ('id', 'username', 'host')

admin.site.register(Author, AuthorAdmin)
