import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from board.models import Contact, Task


CONTACTS = [
    ("Marina Alves", "Lumen Cosméticos", "marina@lumen.com", "(11) 98888-1234"),
    ("Rafael Souza", "NovaTech Soluções", "rafael@novatech.com", "(21) 97777-5678"),
    ("Bianca Ferreira", "Padaria Trigo Dourado", "bianca@trigodourado.com", "(31) 96666-9012"),
    ("Diego Martins", "ConstrutoraMM", "diego@construtoramm.com", "(41) 95555-3456"),
    ("Larissa Costa", "Studio Fit", "larissa@studiofit.com", "(51) 94444-7890"),
]

TASKS = [
    ("Levantar requisitos do sistema de agendamento", "todo", "high", 3),
    ("Criar protótipo de tela no Figma", "todo", "medium", 6),
    ("Configurar ambiente de desenvolvimento", "done", "medium", -5),
    ("Modelar banco de dados", "done", "high", -3),
    ("Implementar autenticação de usuários", "doing", "high", 2),
    ("Integrar gateway de pagamento", "doing", "high", 5),
    ("Escrever testes automatizados da API", "todo", "medium", 8),
    ("Revisar responsividade mobile", "todo", "low", 10),
    ("Deploy em ambiente de homologação", "doing", "medium", 4),
    ("Reunião de alinhamento semanal", "done", "low", -1),
    ("Corrigir bug no relatório de vendas", "todo", "high", 1),
    ("Documentar endpoints da API", "todo", "low", 12),
]


class Command(BaseCommand):
    help = "Popula o banco com contatos e tarefas de exemplo"

    def handle(self, *args, **options):
        Task.objects.all().delete()
        Contact.objects.all().delete()

        contacts = []
        for name, company, email, phone in CONTACTS:
            contacts.append(Contact.objects.create(name=name, company=company, email=email, phone=phone))

        random.seed(7)
        today = date.today()
        for title, status, priority, offset in TASKS:
            Task.objects.create(
                title=title,
                description="Tarefa de exemplo gerada para demonstração do sistema.",
                contact=random.choice(contacts) if random.random() > 0.15 else None,
                status=status,
                priority=priority,
                due_date=today + timedelta(days=offset),
            )

        self.stdout.write(self.style.SUCCESS(
            f"Banco populado: {Contact.objects.count()} contatos, {Task.objects.count()} tarefas."
        ))
