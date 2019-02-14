from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student
from .forms import StudentCreationForm, StudentChangeForm

class MyUserAdmin(UserAdmin):
    add_form = StudentCreationForm
    form = StudentChangeForm
    model = Student

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'middle_name',
            )}),
    )

admin.site.register(Student, MyUserAdmin)