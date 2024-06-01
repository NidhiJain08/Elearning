from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .models import *

from .forms import CourseForm,LessonForm
from django.forms import inlineformset_factory


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {'course': course}

    if request.user.is_authenticated:
        if CourseRegistration.objects.filter(course=course, user=request.user).exists():
            context['is_enrolled'] = True
            context['lessons'] = course.lessons.all()
        else:
            context['is_enrolled'] = False
            context['lessons'] = course.lessons.all()

    return render(request, 'courses/courses.html', context)

def courses_by_category(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    courses = Course.objects.filter(category=category)
    categories = Category.objects.all()

    context = {
        'category': category,
        'courses': courses,
        'categories': categories
    }

    return render(request, 'courses/courses_by_category.html', context)

def create_course(request):
    if request.method=='POST':
        form=CourseForm(request.POST,request.FILES)
        if form.is_valid():
            course=form.save(commit=False)
            course.instructor=request.user
            course.save()
            return HttpResponseRedirect(reverse_lazy('courses:create-lesson', kwargs={'slug': course.slug}))
    else:
        form=CourseForm()
    return render(request,'courses/create_course.html',{'form':form})

def create_lesson(request,slug):
    LessonFormSet=inlineformset_factory(Course,Lesson,fields=('title','video'),extra=3)
    course=Course.objects.get(slug=slug)
    formset=LessonFormSet(queryset=Lesson.objects.none(), instance=course)
    
    if request.method=='POST':
        form=LessonForm(request.POST,request.FILES)
        formset = LessonFormSet(request.POST, request.FILES, instance=course)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    
    context={'form':formset}
    return render(request,'courses/create_lesson.html',context)

        

def search(request):
    query = request.GET.get('query')
    allCoursesTitle = Course.objects.filter(title__icontains=query)
    allCoursesInstructor = Course.objects.filter(instructor__username__icontains=query)
    allCourses = allCoursesTitle.union(allCoursesInstructor)
    if allCourses.count()==0:
        messages.warning(request,  "No search results found. Please refine your query.")
    context = {'allCourses': allCourses, 'query':query}
    return render(request, 'courses/search.html', context)

