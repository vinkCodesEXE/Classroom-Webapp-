from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.views.generic import  (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from Portal.forms import loggerform, StudentForm, TeacherForm, AssignmentForm,SubmitForm, NoticeForm, MessagingForm, MarksForm, TeacherProfileUpdateForm, StudentProfileUpdateForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse
from Portal import models 
from Portal.models import Student, Teacher, SubmitAssignment, StudentsInClass, ClassAssignment,logger, Notice, MessageToTeacher, StudentMarks
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


#For Student Registration 
def StudentSignUp(request):
    user_type = 'Student'
    registered= False

    if request.method == "POST":
        logger_Form = loggerform(data = request.POST)
        Student_Form = StudentForm(data = request.POST)
        if logger_Form.is_valid() and Student_Form.is_valid():

            user = logger_Form.save()
            user.is_student = True
            user.save()

            profile = Student_Form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(logger_Form.errors,Student_Form.errors)
    else:
        logger_Form = loggerform()
        Student_Form = StudentForm()
    return render(request,'student_signup.html',{'logger_Form':loggerform,'Student_Form':StudentForm,'registered':registered,'user_type':user_type})

# FOR teacher Registration 
@csrf_exempt
def TeacherSignUp(request):
    user_type = 'Teacher'
    registered = False 

    if request.method == "POST":
        logger_Form = loggerform(data = request.POST)
        Teacher_Form = TeacherForm(data = request.POST)
        if logger_Form.is_valid() and Teacher_Form.is_valid():
            user = logger_Form.save()
            user.is_teacher = True
            user.save()

            profile = Teacher_Form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(logger_Form.errors,Teacher_Form.errors)
    else:
        logger_Form = loggerform()
        Teacher_Form = TeacherForm()
    return render(request,'teach_signup.html',{'logger_Form':loggerform,'Teacher_Form':TeacherForm,'registered':registered,'user_type':user_type})

# SignUp Page which directs you to whatever you choose Teacher or student signup form
def SignUp(request):
    return render(request,'signup.html',{})

# Login
@csrf_exempt
def User_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('home')

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "Invalid Details")
            return redirect('login')
    else:
        return render(request,'login.html',{})

def home(request):
    return render(request,'index1.html',{})

# logout view.
@login_required
def logger_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

# User Profile of student.
class StudentDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "student"
    model = models.Student
    template_name = 'student_detail_page.html'

# User Profile for teacher.
class TeacherDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "teacher"
    model = models.Teacher
    template_name = 'teacher_detail_page.html'

# Profile update for students.
@login_required
def StudentUpdateView(request,pk):
    profile_updated = False
    student = get_object_or_404(models.Student,pk=pk)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST,instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            profile_updated = True
    else:
        form = StudentProfileUpdateForm(request.POST or None,instance=student)
    return render(request,'student_update_page.html',{'profile_updated':profile_updated,'form':form})

# Profile update for teachers.
@login_required
def TeacherUpdateView(request,pk):
    profile_updated = False
    teacher = get_object_or_404(models.Teacher,pk=pk)
    if request.method == "POST":
        form = TeacherProfileUpdateForm(request.POST,instance=teacher)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            profile_updated = True
    else:
        form = TeacherProfileUpdateForm(request.POST or None,instance=teacher)
    return render(request,'teacher_update_page.html',{'profile_updated':profile_updated,'form':form})

def user_is_teacher(user):
    return user.is_authenticated and user.is_teacher

@user_passes_test(user_is_teacher)
def class_students_list(request):
    query = request.GET.get("q", None)
    students = request.user.Teacher.students.all()
    if query is not None:
        students = students.filter(Q(name__icontains=query))
    context = {
        "class_students_list": students,
    }
    template = "class_students_list.html"
    return render(request, template, context)


class ClassStudentsListView(LoginRequiredMixin,DetailView):
    model = models.Teacher
    template_name = "class_students_list.html"
    context_object_name = "teacher"


# To add student in the class
class add_student(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('students_list')

    def get(self,request,*args,**kwargs):
        student = get_object_or_404(models.Student,pk=self.kwargs.get('pk'))
        try:
            StudentsInClass.objects.create(teacher=self.request.user.Teacher,student=student)
        except:
            messages.warning(self.request,'warning, Student is already in your class!')
        else:
            messages.success(self.request,'{} successfully added student to the class!'.format(student.name))

        return super().get(request,*args,**kwargs)

@login_required
def student_added(request):
    return render(request,'student_added.html',{})

# List of students which are not added by teacher in their class
def students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in students_list:
            pass
        else:
            qs_one.append(x)

    context = {
        "students_list": qs_one,
    }
    template = "students_list.html"
    return render(request, template, context)

# List of all the teacher present in the portal
def teachers_list(request):
    query = request.GET.get("q", None)
    qs = Teacher.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )

    context = {
        "teachers_list": qs,
    }
    template = "teachers_list.html"
    return render(request, template, context)

# for Teacher to create assignment.
@login_required
def upload_assignment(request):
    assignment_uploaded = False
    teacher = request.user.Teacher
    students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)
    if request.method == 'POST':
        print('post method')
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            print('form passed')
            upload = form.save(commit=False)
            upload.teacher = teacher
            students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)
            upload.save()
            print('form successfully saved')
            upload.student.add(*students)
            assignment_uploaded = True
        else:
            print('form not valid')
    else:
        form = AssignmentForm()
        print('not a POST method')
    return render(request,'upload_assignment.html',{'form':form,'assignment_uploaded':assignment_uploaded})

# Students to view the list of the assignments created by the teachers
@login_required
def class_assignment(request):
    student = request.user.Student
    assignment = SubmitAssignment.objects.filter(student=student)
    assignments_list = [x.submitted_assignment for x in assignment]
    return render(request,'class_assignment.html',{'student':student,'assignment_list':assignment_list})


# List of all the assignments created by the teacher
@login_required
def assignment_list(request):
    teacher = request.user.Teacher
    return render(request,'assignment_list.html',{'teacher':teacher})

# For updating the assignments
@login_required
def update_assignment(request,id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    form = AssignmentForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'assignment' in request.FILES:
            obj.assignment = request.FILES['assignment']
        obj.save()
        messages.success(request, "Updated Assignment".format(obj.assignment_name))
        return redirect('assignment_list')
    template = "update_assignment.html"
    return render(request, template, context)

# To delete the assignment
@login_required
def assignment_delete(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Assignment Removed")
        return redirect('assignment_list')
    context = {
        "object": obj,
    }
    template = "assignment_delete.html"
    return render(request, template, context)

# For students to submit their assignments
@login_required
def submit_assignment(request, id=None):
    student = request.user.Student
    assignment = get_object_or_404(ClassAssignment, id=id)
    teacher = assignment.teacher
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.student = student
            upload.submitted_assignment = assignment
            upload.save()
            return redirect('class_assignment')
    else:
        form = SubmitForm()
    return render(request,'submit_assignment.html',{'form':form,})

# To see all the students who have done the submissions
@login_required
def submit_list(request):
    teacher = request.user.Teacher
    return render(request,'submit_list.html',{'teacher':teacher})

# For writing notice which will be sent to all class students.
@login_required
def add_notice(request):
    notice_sent = False
    teacher = request.user.Teacher
    students = StudentsInClass.objects.filter(teacher=teacher)
    students_list = [x.student for x in students]

    if request.method == "POST":
        notice = NoticeForm(request.POST)
        if notice.is_valid():
            object = notice.save(commit=False)
            object.teacher = teacher
            object.save()
            object.students.add(*students_list)
            notice_sent = True
    else:
        notice = NoticeForm()
    return render(request,'write_notice.html',{'notice':notice,'notice_sent':notice_sent})

# Student can see all notice given by their teacher.
@login_required
def class_notice(request,pk):
    student = get_object_or_404(models.Student,pk=pk)
    return render(request,'class_notice_list.html',{'student':student})

# For student writing message to teacher.
@login_required
def write_message(request,pk):
    message_sent = False
    teacher = get_object_or_404(models.Teacher,pk=pk)
    if request.method == "POST":
        form = MessagingForm(request.POST)
        if form.is_valid():
            mssg = form.save(commit=False)
            mssg.teacher = teacher
            mssg.student = request.user.Student
            mssg.save()
            message_sent = True
    else:
        form = MessagingForm()
    return render(request,'write_message.html',{'form':form,'teacher':teacher,'message_sent':message_sent})

# For the list of all the messages teacher have received.
@login_required
def messages_list(request,pk):
    teacher = get_object_or_404(models.Teacher,pk=pk)
    return render(request,'messages_list.html',{'teacher':teacher})

# For Marks obtained by the student in all subjects.
class StudentAllMarksList(LoginRequiredMixin,DetailView):
    model = models.Student
    template_name = "student_allmarks_list.html"
    context_object_name = "student"

# To give marks to a student.
@login_required
def add_marks(request,pk):
    marks_given = False
    student = get_object_or_404(models.Student,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.teacher = request.user.Teacher
            marks.save()
            messages.success(request,'Marks uploaded successfully!')
            return redirect('submit_list')
    else:
        form = MarksForm()
    return render(request,'add_marks.html',{'form':form,'student':student,'marks_given':marks_given})

# For updating marks.
@login_required
def update_marks(request,pk):
    marks_updated = False
    obj = get_object_or_404(StudentMarks,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST,instance=obj)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.save()
            marks_updated = True
    else:
        form = MarksForm(request.POST or None,instance=obj)
    return render(request,'update_marks.html',{'form':form,'marks_updated':marks_updated})

# To see the list of all the marks given by the techer to a specific student.
@login_required
def student_marks_list(request,pk):
    error = True
    student = get_object_or_404(models.Student,pk=pk)
    teacher = request.user.Teacher
    given_marks = StudentMarks.objects.filter(teacher=teacher,student=student)
    return render(request,'student_marks_list.html',{'student':student,'given_marks':given_marks})

