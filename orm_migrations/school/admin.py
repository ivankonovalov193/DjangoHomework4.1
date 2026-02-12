from django.contrib import admin
from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'display_teachers']
    list_filter = ['group']
    search_fields = ['name']
    filter_horizontal = ['teachers']

    def display_teachers(self, obj):
        return ", ".join([teacher.name for teacher in obj.teachers.all()])

    display_teachers.short_description = 'Учителя'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    list_filter = ['subject']
    search_fields = ['name']