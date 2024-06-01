from django.urls import path
from .views import *

app_name = 'courses'
urlpatterns = [
    path('courses/<slug:slug>',course_detail_view, name='course-details'),
    path('courses/<slug:slug>/category', courses_by_category, name='course-by-category'),
    path('upload/',create_course,name='create-course'),
    path('upload/<slug:slug>/lessons/',create_lesson,name='create-lesson'),
    path('search', search, name="search")

]