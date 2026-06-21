from django.db import models
from users.models import CustomerUser
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    # Наследование от самого себя
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.category_name
class Course(models.Model):
    title = models.CharField(max_length=150)
    teacher = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,verbose_name="Учитель курса",related_name="owned_courses")
    extra_teachers = models.ManyToManyField(CustomerUser,related_name="extra_courses", verbose_name="Дополнительные учителя курса",blank=True)
    ready = models.BooleanField(default=False)
    price = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    curent_slides = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

class Student_course(models.Model):
    student = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name="assigned_courses")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.student.username
    
class Student_result(models.Model):
    course_title = models.CharField(max_length=150)
    course_teacher = models.CharField(max_length=150)
    student = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name="student_results")
    test_results = models.JSONField(default=list)
    practice_results = models.JSONField(default=list)

    def __str__(self):
        return f"Результаты: Курс:{self.course_title} - Ученика:{self.student.username}"
    
class Video_course(models.Model):
    title = models.CharField(max_length=150)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_videos", verbose_name="Название курса")
    video = models.FileField(upload_to='videos_uploaded',null=True,
validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])], verbose_name="Видео курса")
    slide = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.title
class Text_course(models.Model):
    title = models.CharField(max_length=150)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_texts", verbose_name="Название курса")
    description = models.TextField(null=True,blank=True,verbose_name="Текст курса")
    slide = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title
class Test_course(models.Model):
    title = models.CharField(max_length=150)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_tests", verbose_name="Название курса")
    data = models.JSONField(default=list)
    slide = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title
    
class Test_answers(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_test_answers", verbose_name="Название курса")
    student = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,verbose_name="Ученик")
    answers = models.JSONField(default=list)
    test = models.ForeignKey(Test_course,on_delete=models.CASCADE, verbose_name="Название теста",default=None)
    results = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.student.username
    
class Test_mock(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_mock_answers", verbose_name="Название курса",null=True, blank=True)
    student = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,verbose_name="Ученик")
    answers = models.JSONField(default=list)
    test = models.ForeignKey(Test_course,on_delete=models.CASCADE, verbose_name="Название теста",default=None)
    results = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.student.username

class Practice_course(models.Model):
    title = models.CharField(max_length=150)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_pactices", verbose_name="Название курса",null=True, blank=True)
    complaints = models.TextField()
    age = models.PositiveBigIntegerField()
    GENDER_ROLES = (('men','Мужчина'),
                  ('women',"Женщина"))
    gender = models.CharField(max_length=10,choices=GENDER_ROLES, default='men')
    diagnosis=models.TextField()
    slide = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

class Practice_answers(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_practice_answers", verbose_name="Название курса",null=True, blank=True)
    practice = models.ForeignKey(Practice_course,on_delete=models.CASCADE,verbose_name="Название задания")
    student = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,verbose_name="Студент")
    tests = models.TextField(verbose_name="Тесты")
    treatment = models.TextField(verbose_name="Лечние")
    results = models.IntegerField(null=True, blank=True)
    commentary = models.TextField(verbose_name="Комментарий",blank=True, null=True)

    def __str__(self):
        return self.student.username




