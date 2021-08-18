from django import forms
from django.contrib.auth.forms import UserCreationForm
from Portal.models import logger,Teacher,Student, ClassAssignment, SubmitAssignment, Notice, MessageToTeacher, StudentMarks
from django.db import transaction

# User Login Form common for both student and teacher login
class loggerform(UserCreationForm):
    class Meta():
        model = logger
        fields = ['username','password1','password2']
        widgets = {
                'username': forms.TextInput(attrs={'class':'answer'}),
                'password1': forms.PasswordInput(attrs={'class':'answer'}),
                'password2': forms.PasswordInput(attrs={'class':'answer'}),
                }

# Teacher SignUp Form 
class TeacherForm(forms.ModelForm):
    class Meta():
        model =  Teacher
        fields = ['name','subject_name','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'subject_name': forms.TextInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

# Student SignUp Form
class StudentForm(forms.ModelForm):
    class Meta():
        model =  Student
        fields = ['name','roll_no','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'roll_no': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

# Form to create updating assignment for teachers        
class AssignmentForm(forms.ModelForm):
    class Meta():
        model = ClassAssignment
        fields = ['assignment_name','assignment']

# Form to submit the assignments for students 
class SubmitForm(forms.ModelForm):
    class Meta():
        model = SubmitAssignment
        fields = ['submit']

# Writing notice in the class        
class NoticeForm(forms.ModelForm):
    class Meta():
        model = Notice
        fields = ['message']

# Writing message to teacher        
class MessagingForm(forms.ModelForm):
    class Meta():
        model = MessageToTeacher
        fields = ['message']

# Form for uploading marks and also for updating it.
class MarksForm(forms.ModelForm):
    class Meta():
        model = StudentMarks
        fields = ['subject_name','marks_obtained','maximum_marks']

# Teacher Profile Update Form
class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name','subject_name','email']

# Student profile update form
class StudentProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name','roll_no','email']

