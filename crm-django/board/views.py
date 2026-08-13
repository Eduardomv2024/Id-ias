from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from .models import Contact, Task


def board(request):
    columns = []
    for value, label in Task.Status.choices:
        tasks = Task.objects.filter(status=value).select_related("contact")
        columns.append({"value": value, "label": label, "tasks": tasks, "count": tasks.count()})

    stats = {
        "total": Task.objects.count(),
        "done": Task.objects.filter(status="done").count(),
        "high_priority_open": Task.objects.filter(priority="high").exclude(status="done").count(),
        "contacts": Contact.objects.count(),
    }
    return render(request, "board/board.html", {"columns": columns, "stats": stats})


def task_update_status(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get("status")
        if new_status in dict(Task.Status.choices):
            task.status = new_status
            task.save()
    return redirect("board")


def task_new(request):
    contacts = Contact.objects.all()
    if request.method == "POST":
        Task.objects.create(
            title=request.POST["title"],
            description=request.POST.get("description", ""),
            contact_id=request.POST.get("contact") or None,
            status=request.POST.get("status", "todo"),
            priority=request.POST.get("priority", "medium"),
            due_date=request.POST.get("due_date") or None,
        )
        messages.success(request, "Tarefa criada com sucesso!")
        return redirect("board")
    return render(request, "board/task_form.html", {"contacts": contacts, "task": None})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    contacts = Contact.objects.all()
    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST.get("description", "")
        task.contact_id = request.POST.get("contact") or None
        task.status = request.POST.get("status", "todo")
        task.priority = request.POST.get("priority", "medium")
        task.due_date = request.POST.get("due_date") or None
        task.save()
        messages.success(request, "Tarefa atualizada!")
        return redirect("board")
    return render(request, "board/task_form.html", {"contacts": contacts, "task": task})


def task_delete(request, pk):
    if request.method == "POST":
        get_object_or_404(Task, pk=pk).delete()
        messages.success(request, "Tarefa removida.")
    return redirect("board")


def contacts(request):
    items = Contact.objects.annotate(
        total_tasks=Count("tasks"),
        open_tasks=Count("tasks", filter=~Q(tasks__status="done")),
    )
    return render(request, "board/contacts.html", {"contacts": items})


def contact_new(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST["name"],
            company=request.POST.get("company", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
        )
        messages.success(request, "Contato cadastrado!")
        return redirect("contacts")
    return render(request, "board/contact_form.html", {"contact": None})


def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.name = request.POST["name"]
        contact.company = request.POST.get("company", "")
        contact.email = request.POST.get("email", "")
        contact.phone = request.POST.get("phone", "")
        contact.save()
        messages.success(request, "Contato atualizado!")
        return redirect("contacts")
    return render(request, "board/contact_form.html", {"contact": contact})


def contact_delete(request, pk):
    if request.method == "POST":
        get_object_or_404(Contact, pk=pk).delete()
        messages.success(request, "Contato removido.")
    return redirect("contacts")
