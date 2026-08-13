from django.urls import path
from . import views

urlpatterns = [
    path("", views.board, name="board"),
    path("tarefas/nova/", views.task_new, name="task_new"),
    path("tarefas/<int:pk>/editar/", views.task_edit, name="task_edit"),
    path("tarefas/<int:pk>/status/", views.task_update_status, name="task_update_status"),
    path("tarefas/<int:pk>/excluir/", views.task_delete, name="task_delete"),
    path("contatos/", views.contacts, name="contacts"),
    path("contatos/novo/", views.contact_new, name="contact_new"),
    path("contatos/<int:pk>/editar/", views.contact_edit, name="contact_edit"),
    path("contatos/<int:pk>/excluir/", views.contact_delete, name="contact_delete"),
]
