from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm,SignInForm
from .models import *
from courses.models import *
# Create your views here.

def home(request):
    return render(request,'home.html')

def registerPage(request):
    form = MyUserCreationForm
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('users:user_page')
        else:
            messages.error(request,'Пожалуйста, исправьте ошибки в форме.')
            return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})
    
def loginPage(request):
    user = request.user
    form = SignInForm()
    if user.is_authenticated:
        return redirect('users:user_page')
    
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', '').strip()
            password = form.cleaned_data.get('password','').strip()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('users:user_page')
            else:
                messages.error(request,'Неверный логин или пароль')
                return render(request,'login.html',{'form':form})
    return render(request, 'login.html', {'form':form})

def signout(request):
    logout(request)
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def send_email(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        receiver = course.teacher.email
        try:
            send_mail(subject,message,None,[receiver])
            messages.success(request,'Письмо было успешно отправленно.')
            return redirect('courses:student_courses')
        except:
            messages.error(request,'Что-то пошло не так.')
            return redirect('courses:user_page')
    return render(request, 'send_email.html')

@login_required(login_url='users:signup')
def user_page(request):
    user = request.user
    mock_scores = Test_mock.objects.filter(student=user)
    course_scores = {}
    for score in mock_scores:
        course_scores.setdefault(
            score.course.id,
            []
        ).append(score)
        print(course_scores)
    else:
        courses = user.assigned_courses.filter(finished = False)
        finished_courses = user.assigned_courses.filter(finished = True)
        finished_results = user.student_results.all()
    for course in finished_courses:
        course.answers = course_scores.get(course.course.id, [])
    return render(request,'user_page.html',{'finished_results':finished_results,"courses":courses,'finished_courses':finished_courses})