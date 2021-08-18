"""IB_Portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Portal import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('SignUp/',views.SignUp,name="SignUp"),
    path('home/', views.home, name= 'home'),
    path('signup/student_signup/',views.StudentSignUp,name="StudentSignUp"),
    path('signup/teacher_signup/',views.TeacherSignUp,name="TeacherSignUp"),
    path('',views.User_login,name="login"),
    path('logout/',views.logger_logout,name="logout"),
    path('student/<int:pk>/',views.StudentDetailView.as_view(),name="student_detail"),
    path('student/<int:pk>/add',views.add_student.as_view(),name="add_student"),
    path('student_added/',views.student_added,name="student_added"),
    path('students_list/',views.students_list,name="students_list"),
    path('teachers_list/',views.teachers_list,name="teachers_list"),
    path('teacher/class_students_list',views.class_students_list,name="class_student_list"),
    path('upload_assignment/',views.upload_assignment,name="upload_assignment"),
    path('class_assignment/',views.class_assignment,name="class_assignment"),
    path('assignment_list/',views.assignment_list,name="assignment_list"),
    path('update_assignment/<int:id>/',views.update_assignment,name="update_assignment"),
    path('assignment_delete/<int:id>/',views.assignment_delete,name="assignment_delete"),
    path('submit_assignment/<int:id>/',views.submit_assignment,name="submit_assignment"),
    path('submit_list/',views.submit_list,name="submit_list"),
    path('teacher/<int:pk>/',views.TeacherDetailView.as_view(),name="teacher_detail"),
    path('teacher/notice',views.add_notice,name="write_notice"),
    path('student/<int:pk>/notice',views.class_notice,name="class_notice"),
    path('student/<int:pk>/message',views.write_message,name="write_message"),
    path('teacher/<int:pk>/messages_list',views.messages_list,name="messages_list"),
    path('student/<int:pk>/all_marks',views.StudentAllMarksList.as_view(),name="all_marks_list"),
    path('student/<int:pk>/enter_marks',views.add_marks,name="enter_marks"),
    path('student/<int:pk>/marks_list',views.student_marks_list,name="student_marks_list"),
    path('marks/<int:pk>/update',views.update_marks,name="update_marks"),
    path('update/student/<int:pk>/',views.StudentUpdateView,name="student_update"),
    path('update/teacher/<int:pk>/',views.TeacherUpdateView,name="teacher_update"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
