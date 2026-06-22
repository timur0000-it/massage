from django.urls import path,include
from .views import *
app_name = 'courses'

urlpatterns = [
    path('create_test/<int:course_id>/', create_test,name='create_test'),
    path('create_course/', create_course,name='create_course'),
    path('course_main/<int:course_id>/', course_main,name='course_main'),
    path('delete_course/<int:pk>/', delete_course,name='delete_course'),
    path('check_answer/<int:answer_id>/', check_answer,name='check_answer'),
    path('course_start/<int:course_id>/', course_start,name='course_start'),
    path('course_ready/<int:course_id>/', course_ready,name='course_ready'),
    path('course_not_ready/<int:course_id>/', course_not_ready,name='course_not_ready'),
    path('course_end/<int:course_id>/', course_end,name='course_end'),
    path('add_extra_teacher/<int:course_id>/', add_extra_teacher,name='add_extra_teacher'),
    path('my_courses/', my_courses,name='my_courses'),
    path('course_video/<int:pk>/', course_video,name='course_video'),
    path('delete_test/<int:pk>/', delete_test,name='delete_test'),
    path('delete_video/<int:pk>/', delete_video,name='delete_video'),
    path('delete_text/<int:pk>/', delete_text,name='delete_text'),
    path('delete_practice/<int:pk>/', delete_practice,name='delete_practice'),
    path('course_test/<int:pk>/', course_test,name='course_test'),
    path('course_text/<int:pk>/', course_text,name='course_text'),
    path('course_practice/<int:pk>/', course_practice,name='course_practice'),
    path('create_text/<int:course_id>/', create_text,name='create_text'),
    path('create_practice/<int:course_id>/', create_practice,name='create_practice'),
    path('create_video/<int:course_id>/', create_video,name='create_video'),
    path('course_finish/<int:course_id>/', course_finish,name='course_finish'),
    path('add_slide/<str:word>/<int:pk>/', add_slide,name='add_slide'),
    path('delete_slide/<int:course_id>/<int:slide>/', delete_slide,name='delete_slide'),
    path('next_slide/<int:course_id>/<int:slide>/', next_slide,name='next_slide'),
    path('previous_slide/<int:course_id>/<int:slide>/', previous_slide,name='previous_slide'),
    path('update_test/<int:pk>/', update_test,name='update_test'),
    path('update_text/<int:pk>/', update_text,name='update_text'),
    path('update_course/<int:pk>/', update_course,name='update_course'),
    path('update_practice/<int:pk>/', update_practice,name='update_practice'),
    path('update_video/<int:pk>/', update_video,name='update_video'),

]