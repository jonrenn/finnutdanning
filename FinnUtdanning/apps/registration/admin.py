from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student


class MyUserAdmin(UserAdmin):
    model = Student

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'middle_name',
            )}),
    )

admin.site.register(Student, MyUserAdmin)