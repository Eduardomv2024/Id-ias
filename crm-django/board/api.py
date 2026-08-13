from rest_framework import viewsets
from .models import Contact, Task
from .serializers import ContactSerializer, TaskSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("contact").all()
    serializer_class = TaskSerializer
