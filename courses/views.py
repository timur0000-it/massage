from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
# Create your views here.

def teacher_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_teacher:
            return func(request,*args,**kwargs)
        messages.error(request,'Вам здесь не место')
        return redirect('users:user_page')
    return wrapper

@login_required(login_url='users:signup')
@teacher_required
def create_course(request):
    form = CourseForm()
    if request.method =='POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course= form.save(commit=False)
            course.teacher=request.user
            course.save()
            return redirect('courses:course_main',course_id=course.id)
    return render(request,'creation_form.html',{'form':form})

@login_required(login_url='users:signup')
def update_course(request,pk):
    course = Course.objects.filter(id=pk).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST,instance=course)
        if form.is_valid():
          form.save()
          messages.success(request, 'Course updated successfully!')
          return redirect('courses:course_main',course_id=course.id)
        else:
            print(form.errors)
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    return render(request,'creation_form.html',{'form':form})


@login_required(login_url='users:signup')
def delete_course(request,pk):
    course = Course.objects.filter(id=pk).first()
    if not course:
        return redirect('users:user_page')
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if Practice_answers.objects.filter(course=course, results__isnull=True).exists():
            messages.error(request,'Нужно проверить все ответы перед тем как удалить курс')
            return redirect('courses:my_courses')
    course.delete()
    messages.success(request, 'Курс успешно удалён')
    return redirect('courses:my_courses')


@login_required(login_url='users:signup')
def my_courses(request):
    user = request.user
    extra_courses = user.extra_courses.all()
    courses = user.owned_courses.all()
    answers = Practice_answers.objects.filter(results = None)
    course_answers = {}
    for answer in answers:
        course_answers.setdefault(
            answer.practice.course.id,
            []
        ).append(answer)

    for course in courses:
        course.answers = course_answers.get(course.id, [])
    for course in extra_courses:
        course.answers = course_answers.get(course.id, [])
    if user.is_teacher:
        return render(request,'my_courses.html',{'courses':courses,'extra_courses':extra_courses})
    else:
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')

@login_required(login_url='users:signup')
def course_main(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if course:
        videos = Video_course.objects.filter(course=course,slide=0)
        texts = Text_course.objects.filter(course=course,slide=0)
        tests = Test_course.objects.filter(course=course,slide=0)
        practices = Practice_course.objects.filter(course=course,slide=0)

        video = Video_course.objects.filter(course=course,slide__gt=0)
        text = Text_course.objects.filter(course=course,slide__gt=0)
        test = Test_course.objects.filter(course=course,slide__gt=0)
        practice = Practice_course.objects.filter(course=course,slide__gt=0)
        slides={}
        for v in video:
            slides[v.slide]=v
        for v in text:
            slides[v.slide]=v
        for v in test:
            slides[v.slide]=v
        for v in practice:
            slides[v.slide]=v
        slides = dict(sorted(slides.items()))
        return render(request,'course_main.html',{'videos':videos,'texts':texts,'tests':tests,'practices':practices,'course':course,'slides':slides})
    return redirect('users:user_page')




@login_required(login_url='users:signup')
def add_slide(request,word,pk):
    if word == 'video':
        video = Video_course.objects.filter(id=pk).first()
        if video.slide == 0:
            course=video.course
            if request.user != course.teacher and request.user not in course.extra_teachers.all():
                messages.error(request, 'У вас нет прав')
                return redirect('users:user_page')
            course.curent_slides += 1
            course.save()
            video.slide = course.curent_slides
            video.save()
            return redirect('courses:course_main',course_id=course.id)
    elif word == 'text':
        text = Text_course.objects.filter(id=pk).first()
        if text.slide == 0:
            course=text.course
            if request.user != course.teacher and request.user not in course.extra_teachers.all():
                messages.error(request, 'У вас нет прав')
                return redirect('users:user_page')
            course.curent_slides += 1
            course.save()
            text.slide = course.curent_slides
            text.save()
            return redirect('courses:course_main',course_id=course.id)
    elif word == 'test':
        test = Test_course.objects.filter(id=pk).first()
        if test.slide == 0:
            course=test.course
            if request.user != course.teacher and request.user not in course.extra_teachers.all():
                messages.error(request, 'У вас нет прав')
                return redirect('users:user_page')
            course.curent_slides += 1
            course.save()
            test.slide = course.curent_slides
            test.save()
            return redirect('courses:course_main',course_id=course.id)
    elif word == 'practice':
        practice = Practice_course.objects.filter(id=pk).first()
        if practice.slide == 0:
            course=practice.course
            if request.user != course.teacher and request.user not in course.extra_teachers.all():
                messages.error(request, 'У вас нет прав')
                return redirect('users:user_page')
            course.curent_slides += 1
            course.save()
            practice.slide = course.curent_slides
            practice.save()
            return redirect('courses:course_main',course_id=course.id)
    return render(request,'course_main.html',course_id=course.id)

@login_required(login_url='users:signup')
def delete_slide(request,course_id,slide):
        course = Course.objects.filter(id=course_id).first()
        if request.user != course.teacher and request.user not in course.extra_teachers.all():
            messages.error(request, 'У вас нет прав')
            return redirect('users:user_page')
        if course:
            video = Video_course.objects.filter(course=course,slide=slide).first()
            text = Text_course.objects.filter(course=course,slide=slide).first()
            test = Test_course.objects.filter(course=course,slide=slide).first()
            practice = Practice_course.objects.filter(course=course,slide=slide).first()
        if video:
            if video.slide != 0:
                slide_num = video.slide
                video.slide = 0
                video.save()
                course=video.course
                course.curent_slides -= 1
                course.save()
                reorder_slides(course,slide_num)
                return redirect('courses:course_main',course_id=course.id)
        elif text:
            if text.slide != 0:
                slide_num = text.slide
                text.slide = 0
                text.save()
                course=text.course
                course.curent_slides -= 1
                course.save()
                reorder_slides(course,slide_num)
                return redirect('courses:course_main',course_id=course.id)
        elif test:
            if test.slide != 0:
                slide_num = test.slide
                test.slide = 0
                test.save()
                course=test.course
                course.curent_slides -= 1
                course.save()
                reorder_slides(course,slide_num)
                return redirect('courses:course_main',course_id=course.id)
        elif practice:
            practice = Practice_course.objects.filter(slide=slide).first()
            if practice.slide != 0:
                slide_num = practice.slide
                practice.slide = 0
                practice.save()
                course=practice.course
                course.curent_slides -= 1
                course.save()
                reorder_slides(course,slide_num)
                return redirect('courses:course_main',course_id=course.id)
        return render(request,'course_main.html',course_id=course.id)


def reorder_slides(course, slide_num):
    Video_course.objects.filter(
        course=course,
        slide__gt=slide_num
    ).update(slide=F('slide') - 1)

    Text_course.objects.filter(
        course=course,
        slide__gt=slide_num
    ).update(slide=F('slide') - 1)

    Test_course.objects.filter(
        course=course,
        slide__gt=slide_num
    ).update(slide=F('slide') - 1)

    Practice_course.objects.filter(
        course=course,
        slide__gt=slide_num
    ).update(slide=F('slide') - 1)

@login_required(login_url='users:signup')
def next_slide(request,course_id,slide):
    course = Course.objects.filter(id=course_id).first()
    is_teacher = is_teacher = request.user == course.teacher or request.user in course.extra_teachers.all()
    is_student = Student_course.objects.filter(student=request.user,course=course).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    slide += 1
    if course.curent_slides < slide:
        return redirect('courses:course_end' ,course_id=course.id)
    elif slide < 0:
        return redirect('courses:course_main',course_id=course.id)
    video = Video_course.objects.filter(course=course,slide=slide).first()
    text = Text_course.objects.filter(course=course,slide=slide).first()
    test = Test_course.objects.filter(course=course,slide=slide).first()
    practice = Practice_course.objects.filter(course=course,slide=slide).first()
    if video:
        return redirect('courses:course_video' ,pk=video.id)
    elif text:
        return redirect('courses:course_text' ,pk=text.id)
    elif test:
        return redirect('courses:course_test' ,pk=test.id)
    elif practice:
        return redirect('courses:course_practice' ,pk=practice.id)

@login_required(login_url='users:signup')
def previous_slide(request,course_id,slide):
    course = Course.objects.filter(id=course_id).first()
    is_teacher = is_teacher = request.user == course.teacher or request.user in course.extra_teachers.all()
    is_student = Student_course.objects.filter(student=request.user,course=course).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    slide -= 1
    if slide == 0 :
        return render(request,'course_start.html',{'course':course})
    elif course.curent_slides < slide:
        return render(request,'course_end.html',{'course':course})
    video = Video_course.objects.filter(course=course,slide=slide).first()
    text = Text_course.objects.filter(course=course,slide=slide).first()
    test = Test_course.objects.filter(course=course,slide=slide).first()
    practice = Practice_course.objects.filter(course=course,slide=slide).first()
    if video:
        return redirect('courses:course_video' ,pk=video.id)
    elif text:
        return redirect('courses:course_text' ,pk=text.id)
    elif test:
        return redirect('courses:course_test' ,pk=test.id)
    elif practice:
        practice_answers = Practice_answers.objects.filter(student=request.user,practice=practice).first()
        form = Practice_StudentForm(instance=practice_answers)
        return redirect('courses:course_practice' ,pk=practice.id)



@login_required(login_url='users:signup')
def create_test(request,course_id):
    numbers = range(1,11)
    numbers2 = range(1,5)
    course = Course.objects.filter(id=course_id).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if request.method =='POST':
        test=[]
        title = request.POST.get('title', "").strip()
        for i in range(1,11):
            question = request.POST.get(f"{i}", "").strip()
            answers = request.POST.getlist(f'answer_{i}')
            right_answer = int(request.POST.get(f'right_{i}'))
            questions = {'question':question,'answers':answers,'right':right_answer}
            test.append(questions)
        Test_course.objects.create(course=course,data=test,title=title)
        return redirect('courses:course_main',course_id=course.id)
    return render(request,'create_test.html',{'numbers':numbers,'numbers2':numbers2})

@login_required(login_url='users:signup')
def create_text(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    form = TextForm()
    if request.method =='POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text= form.save(commit=False)
            text.course=course
            text.save()
            return redirect('courses:course_main',course_id=course.id)
    return render(request,'creation_form.html',{'form':form})

@login_required(login_url='users:signup')
def create_video(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    form = VideoForm()
    if request.method =='POST':
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course=course
            video.save()
            return redirect('courses:course_main',course_id=course.id)

    return render(request,'creation_form.html',{'form':form})

@login_required(login_url='users:signup')
def create_practice(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    form = PracticeForm()
    if request.method =='POST':
        form = PracticeForm(request.POST)
        if form.is_valid():
            practice = form.save(commit=False)
            practice.course=course
            practice.save()
            return redirect('courses:course_main',course_id=course.id)
    return render(request,'creation_form.html',{'form':form})



@login_required(login_url='users:signup')
def update_text(request,pk):
    text = Text_course.objects.filter(id=pk).first()
    if request.user != text.course.teacher and request.user not in text.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    form = TextForm(instance=text)
    if request.method == 'POST':
        form = TextForm(request.POST,instance=text)
        if form.is_valid():
          form.save()
          messages.success(request, 'Text updated successfully!')
          return redirect('courses:course_main',course_id=text.course.id)
        else:
            print(form.errors)
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    return render(request,'creation_form.html',{'form':form})

@login_required(login_url='users:signup')
def update_practice(request,pk):
    practice = Practice_course.objects.filter(id=pk).first()
    if request.user != practice.course.teacher and request.user not in practice.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    form = PracticeForm(instance=practice)
    if request.method == 'POST':
        form = PracticeForm(request.POST,instance=practice)
        if form.is_valid():
          form.save()
          messages.success(request, 'practice updated successfully!')
          return redirect('courses:course_main',course_id=practice.course.id)
        else:
            print(form.errors)
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    return render(request,'creation_form.html',{'form':form})


@login_required(login_url='users:signup')
def update_video(request,pk):
    video = Video_course.objects.filter(id=pk).first()
    form = VideoForm(instance=video)
    if request.user != video.course.teacher and request.user not in video.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if request.method == 'POST':
        form = VideoForm(request.POST,request.FILES,instance=video)
        if form.is_valid():
          form.save()
          messages.success(request, 'video updated successfully!')
          return redirect('courses:course_main',course_id=video.course.id)
        else:
            print(form.errors)
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    return render(request,'creation_form.html',{'form':form})

@login_required(login_url='users:signup')
def update_test(request,pk):
    test = Test_course.objects.filter(id=pk).first()
    if request.user != test.course.teacher and request.user not in test.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if request.method =='POST':
        test_data=[]
        title = request.POST.get('title', "").strip()
        for i in range(1,11):
            question = request.POST.get(f"{i}", "").strip()
            answers = request.POST.getlist(f'answer_{i}')
            right_answer = int(request.POST.get(f'right_{i}'))
            questions = {'question':question,'answers':answers,'right':right_answer}
            test_data.append(questions)
            test.title = title
            test.data = test_data
            test.save()
        return redirect('courses:course_main',course_id=test.course.id)
    return render(request,'update_test.html',{'test':test})

@login_required(login_url='users:signup')
def course_video(request,pk):
    video = Video_course.objects.filter(id=pk).first()
    is_teacher = is_teacher = request.user == video.course.teacher or request.user in video.course.extra_teachers.all()
    
    is_student = Student_course.objects.filter(student=request.user,course=video.course).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if video:
        return render(request,'course_video.html',{'video':video,'course_id':video.course.id,'is_teacher':is_teacher})
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def course_test(request,pk):
    test = Test_course.objects.filter(id=pk).first()
    right_answers=[]
    for answer in test.data:
        right_answers.append(answer['right'])
    is_teacher = is_teacher = request.user == test.course.teacher or request.user in test.course.extra_teachers.all()
    is_student = Student_course.objects.filter(student=request.user,course=test.course).exists()
    is_finished = Student_course.objects.filter(student=request.user,course=test.course,finished=True).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if test:
        if request.method =='POST':
            results = 0
            test_answers=[]
            for i in range(1,11):
                right_answer = request.POST.get(f'right_{i}')
                if int(right_answer) == right_answers[i-1]:
                    results+=1
                test_answers.append(right_answer)
            if is_finished:
                Test_mock.objects.create(course=test.course,test=test,student=request.user,answers=test_answers,results=results)
                return redirect('courses:next_slide',course_id=test.course.id,slide=test.slide)
            Test_answers.objects.update_or_create(course=test.course,student=request.user,test=test,defaults={'answers': test_answers,'results': results,})
            return redirect('courses:next_slide',course_id=test.course.id,slide=test.slide)
        return render(request,'course_test.html',{'test':test,'course_id':test.course.id,'is_teacher':is_teacher,'is_finished':is_finished})
    else:
        return redirect('users:user_page')
    


@login_required(login_url='users:signup')
def course_text(request,pk):
    text = Text_course.objects.filter(id=pk).first()
    is_teacher = is_teacher = request.user == text.course.teacher or request.user in text.course.extra_teachers.all()
    is_student = Student_course.objects.filter(student=request.user,course=text.course).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if text:
        return render(request,'course_text.html',{'text':text,'course_id':text.course.id,'is_teacher':is_teacher})
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def course_practice(request,pk):
    practice = Practice_course.objects.filter(id=pk).first()
    form = Practice_StudentForm()
    answers =  Practice_answers.objects.filter(practice=practice,student=request.user).first()
    if answers:
        form = Practice_StudentForm(instance=answers)
    is_teacher = request.user == practice.course.teacher or request.user in practice.course.extra_teachers.all()
    is_student = Student_course.objects.filter(student=request.user,course=practice.course).exists()
    is_finished = Student_course.objects.filter(student=request.user,course=practice.course,finished=True).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if practice:
        if request.method =='POST':
            answers =  Practice_answers.objects.filter(practice=practice,student=request.user)
            if answers:
                answers.delete()
            form = Practice_StudentForm(request.POST)
            if form.is_valid():
                practice_answers = form.save(commit=False)
                practice_answers.practice=practice
                practice_answers.course = practice.course
                practice_answers.student=request.user
                practice_answers.save()
                return redirect('courses:next_slide',course_id=practice.course.id,slide=practice.slide)
        return render(request,'course_practice.html',{'practice':practice,'form':form,'course_id':practice.course.id,'is_teacher':is_teacher,'is_finished':is_finished})
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def delete_video(request,pk):
    video = Video_course.objects.filter(id=pk).first()
    if request.user != video.course.teacher and request.user not in video.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if video:
        video.delete()
        return redirect('courses:course_main',course_id=video.course.id)
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def delete_test(request,pk):
    test = Test_course.objects.filter(id=pk).first()
    if request.user != test.course.teacher and request.user not in test.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if test:
        test.delete()
        return redirect('courses:course_main',course_id=test.course.id)
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def delete_text(request,pk):
    text = Text_course.objects.filter(id=pk).first()
    if request.user != text.course.teacher and request.user not in text.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if text:
        text.delete()
        return redirect('courses:course_main',course_id=text.course.id)
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def delete_practice(request,pk):
    practice = Practice_course.objects.filter(id=pk).first()
    if request.user != practice.course.teacher and request.user not in practice.course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if practice:
        practice.delete()
        return redirect('courses:course_main',course_id=practice.course.id)
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def course_start(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    is_teacher = request.user == course.teacher or request.user in course.extra_teachers.all()
    is_student = Student_course.objects.filter(student=request.user,course=course).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if course:
        return render(request,'course_start.html',{'course':course})
    return redirect('users:user_page')


@login_required(login_url='users:signup')
def course_finish(request,course_id):
    user = request.user
    course = Course.objects.filter(id=course_id).first()
    student_course = Student_course.objects.filter(student=user,course=course).exists()
    if not (student_course):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if course:
        student_course = Student_course.objects.filter(student=user,course=course).first()
        practice_scores = Practice_answers.objects.filter(student=user,course=course)
        test_scores = Test_answers.objects.filter(student=user,course=course)
        practice = []
        test = []
        for score in practice_scores:
            obj = {'title':score.practice.title,'results':score.results,'commentary':score.commentary}
            practice.append(obj)
        for score in test_scores:
            obj = {'title':score.test.title,'results':score.results,'quantity':len(score.answers)}
            test.append(obj)
        Student_result.objects.create(course_title = course.title,course_teacher = course.teacher,student=user,test_results=test,practice_results=practice)
        student_course.finished = True
        student_course.save()
        redirect('users:user_page')
    print(3)
    return redirect('users:user_page')

@login_required(login_url='users:signup') 
def course_end(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    is_teacher = request.user == course.teacher or request.user in course.extra_teachers.all()
    is_student = Student_course.objects.filter(student=request.user,course=course).exists()
    is_finished = Student_course.objects.filter(student=request.user,course=course,finished=True).exists()
    if not (is_teacher or is_student):
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if course:
        course_slide = course.curent_slides + 1
        return render(request,'course_end.html',{'course':course,'course_slide':course_slide,'is_teacher':is_teacher,'is_finished':is_finished})
    return redirect('users:user_page')

@login_required(login_url='users:signup')
def course_ready(request,course_id):
    course = Course.objects.filter(id=course_id).first()

    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if course:
        if course.ready == True:
            messages.error(request, 'У вас уже создан этот проект!')
            return redirect('users:user_page')
        if course.curent_slides < 1:
            messages.error(request, f'Проект "{course.title}" должен иметь хоть 1 слайд.')
            return redirect('courses:course_main',course_id=course_id)
        if request.method == "POST":
            course.ready = True
            price = request.POST.get('price')
            course.price = price
            course.save()
            messages.success(request, f'Проект "{course.title}" был успешно создан.')
            return redirect('courses:course_main',course_id=course_id)
    return render(request,'course_ready.html',{"obj":course})


@login_required(login_url='users:signup')
def add_extra_teacher(request,course_id):
    user = request.user
    course = Course.objects.filter(id=course_id).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    users = CustomerUser.objects.filter(teacher=True).exclude(id=user.id)

    if request.method == "POST":
        extra_teacher = request.POST.get('extra')
        extra = CustomerUser.objects.filter(id=extra_teacher).first()
        course.extra_teachers.add(extra)
        return redirect('courses:course_main',course_id=course_id)
    return render(request,'add_extra_teacher.html',{"users":users})

@login_required(login_url='users:signup')
def course_not_ready(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    if request.user != course.teacher and request.user not in course.extra_teachers.all():
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    if course:
        if course.ready == True:
            course.ready = False
            course.save()
            messages.success(request, f'Проект "{course.title}" был снят')
            return redirect('courses:course_main',course_id=course_id)

@login_required(login_url='users:signup')
def check_answer(request,answer_id):
    answer = Practice_answers.objects.filter(id=answer_id).first()
    if answer:
        course = answer.practice.course
        practice = answer.practice
        student = answer.student
        if request.user != course.teacher and request.user not in course.extra_teachers.all():
            messages.error(request, 'У вас нет прав')
            return redirect('users:user_page')
        if request.method == 'POST':
            results = request.POST.get('results')
            commentary = request.POST.get('commentary')
            answer.results = results
            answer.commentary = commentary
            answer.save()
            student_results = student.student_results.filter(course_title = course.title).first()
            for result in student_results.practice_results:
                if result['title'] == practice.title:
                    result['results'] = results
                    result['commentary'] = commentary
            student_results.save()
            return redirect('courses:my_courses')
        return render(request,'check_answer.html',{'answer':answer,'practice':practice})
    else:
        messages.error(request, 'У вас нет прав')
        return redirect('users:user_page')
    
