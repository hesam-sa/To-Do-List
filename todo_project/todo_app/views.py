from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404
from .forms import RegisterForm
from django.contrib.auth import login


@login_required
def task_list(request):

    search_query = request.GET.get('search','')
    filter_status = request.GET.get('status','')

    tasks = Task.objects.filter(user=request.user)

    if search_query :
        tasks = tasks.filter(title__icontains=search_query)

    if filter_status == 'completed' :
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending' :
        tasks = tasks.filter(completed=False)    

    tasks = tasks.order_by('-created_at')

    #Statistics
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user,completed=True).count() 
    pending_tasks = total_tasks - completed_tasks


    return render(request,'todo_app/index.html',{'tasks':tasks , 'search_query':search_query , 'filter_status':filter_status,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks})


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


def register_view(requset):
    if requset.method == 'POST' :
        form = RegisterForm(requset.POST)
        if form.is_valid():
            user = form.save()
            login(requset,user)
            return redirect('task_list')
    else:
        form=RegisterForm()
    return render(requset,'todo_app/register.html',{'form':form})
