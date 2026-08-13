from django.contrib import admin
from .models import Contact, Task


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "phone", "open_tasks_count")
    search_fields = ("name", "company", "email")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "contact", "status", "priority", "due_date")
    list_filter = ("status", "priority")
    search_fields = ("title", "description")
