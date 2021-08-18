from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import logger,Student,Teacher, StudentsInClass, ClassAssignment, MessageToTeacher, Notice, StudentMarks,SubmitAssignment
# Register your models here.

admin.site.register(logger, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentsInClass)
admin.site.register(ClassAssignment)
admin.site.register(MessageToTeacher)
admin.site.register(Notice)
admin.site.register(SubmitAssignment)
admin.site.register(StudentMarks)