from django.db import models


class Contact(models.Model):
    name = models.CharField("Nome", max_length=120)
    company = models.CharField("Empresa", max_length=120, blank=True)
    email = models.EmailField("E-mail", blank=True)
    phone = models.CharField("Telefone", max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def open_tasks_count(self):
        return self.tasks.exclude(status="done").count()


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "A fazer"
        DOING = "doing", "Em andamento"
        DONE = "done", "Concluído"

    class Priority(models.TextChoices):
        LOW = "low", "Baixa"
        MEDIUM = "medium", "Média"
        HIGH = "high", "Alta"

    title = models.CharField("Título", max_length=160)
    description = models.TextField("Descrição", blank=True)
    contact = models.ForeignKey(
        Contact, related_name="tasks", on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Contato",
    )
    status = models.CharField("Status", max_length=10, choices=Status.choices, default=Status.TODO)
    priority = models.CharField("Prioridade", max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField("Prazo", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
