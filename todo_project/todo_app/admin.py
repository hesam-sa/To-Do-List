from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title' , 'user' , 'completed' , 'created_at' , 'due_date')
    list_filter = ('completed' , 'created_at')
    search_fields = ('title' , 'description')