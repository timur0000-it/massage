from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display=('category_name',)
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('title','teacher','ready','curent_slides')
    list_editable = ('ready','curent_slides')
    list_filter = ('teacher',)
    search_fields = ('title','teacher')

@admin.register(Student_course)
class Student_courseAdmin(admin.ModelAdmin):
    model = Student_course
    
@admin.register(Student_result)
class Student_resultAdmin(admin.ModelAdmin):
    model = Student_result

@admin.register(Video_course)
class Video_courseAdmin(admin.ModelAdmin):
    model = Video_course
    list_display = ('title','course','video','slide')
    list_editable = ('course',)
    list_filter = ('course',)
    search_fields = ('title','course')

@admin.register(Text_course)
class Text_courseAdmin(admin.ModelAdmin):
    model = Text_course
    list_display = ('title','course','description','slide')
    list_editable = ('course',)
    list_filter = ('course',)
    search_fields = ('title','course')

@admin.register(Test_course)
class Test_courseAdmin(admin.ModelAdmin):
    model = Test_course
    list_display = ('title','course','slide')
    list_editable = ('course',)
    list_filter = ('course',)
    search_fields = ('title','course')

@admin.register(Test_answers)
class Test_answersAdmin(admin.ModelAdmin):
    model = Test_answers
    list_display = ('student','test')
    list_editable = ('test',)
    list_filter = ('test',)
    search_fields = ('test',)

@admin.register(Practice_course)
class Practice_courseAdmin(admin.ModelAdmin):
    model = Practice_course
    list_display = ('title','course','slide')
    list_editable = ('course',)
    list_filter = ('course',)
    search_fields = ('title','course')

@admin.register(Practice_answers)
class Practice_answersAdmin(admin.ModelAdmin):
    model = Practice_answers
    list_display = ('student','practice')
    search_fields = ('student','practice')