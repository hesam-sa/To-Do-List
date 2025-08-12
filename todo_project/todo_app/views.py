from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'todo_app/task_list.html',{'tasks':tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    
    return render(request, 'todo_app/add_task.html', {'form': form})

@login_required
def edit_task(request,task_id):
    task = get_object_or_404(Task,id=task_id,user=request.user)
    if request.method == 'POST' :
        form = TaskForm(request.POST , instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request,"todo_app/edit_task.html",{'form':form})

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,id=task_id,user=request.user)
    if request.method == 'POST' :
        task.delete()
        return redirect('task_list')
    return render(request,"todo_app/delete_task.html",{'task': task})

