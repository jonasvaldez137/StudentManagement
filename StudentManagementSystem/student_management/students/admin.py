from django.contrib import admin
from .models import Student, Subject, Enrollment, Grade

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'email', 'created_at']
    search_fields = ['first_name', 'last_name', 'student_id', 'email']
    list_filter = ['created_at']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits']
    search_fields = ['code', 'name']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'enrolled_at']
    list_filter = ['enrolled_at', 'subject']
    search_fields = ['student__first_name', 'student__last_name', 'subject__name']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'grade_type', 'name', 'score', 'max_score', 'percentage']
    list_filter = ['grade_type', 'date_recorded']
    search_fields = ['enrollment__student__first_name', 'enrollment__student__last_name', 'name']


