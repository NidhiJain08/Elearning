from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.apps import apps
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def signup(request):
    if request.method=='POST':
       form = CreateUserForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('account:login')
    else:
        form = CreateUserForm()
        
    context = {'form': form}
    return render(request,'account/signup.html',context)

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))