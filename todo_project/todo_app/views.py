from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'todo_app/task_list.html',{'tasks':tasks})