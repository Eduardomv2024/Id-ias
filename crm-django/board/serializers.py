from rest_framework import serializers
from .models import Contact, Task


class ContactSerializer(serializers.ModelSerializer):
    open_tasks_count = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = ["id", "name", "company", "email", "phone", "created_at", "open_tasks_count"]


class TaskSerializer(serializers.ModelSerializer):
    contact_name = serializers.ReadOnlyField(source="contact.name")

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "contact", "contact_name",
            "status", "priority", "due_date", "created_at",
        ]
