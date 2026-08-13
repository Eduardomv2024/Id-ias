# TaskFlow CRM — Gestão de Contatos e Tarefas

Mini-CRM full stack com board estilo Kanban para gestão de tarefas
vinculadas a contatos/clientes.

**Stack:** Python, Django, Django REST Framework, SQLite, templates
server-side + CSS puro.

## Funcionalidades

- Board Kanban (A fazer / Em andamento / Concluído) com mudança de status
  em um clique
- Cadastro de contatos (nome, empresa, e-mail, telefone)
- Tarefas vinculadas a contatos, com prioridade e prazo
- Painel administrativo do Django pronto (`/admin/`)
- API REST completa via Django REST Framework (`/api/tasks/`,
  `/api/contacts/`)

## Como rodar localmente

```bash
cd crm-django
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django djangorestframework
python manage.py migrate
python manage.py seed           # popula com dados de exemplo
python manage.py createsuperuser  # opcional, para acessar /admin/
python manage.py runserver      # inicia em http://localhost:8000
```

## Texto para o portfólio do Workana

> **TaskFlow CRM — Gestão de Contatos e Tarefas**
> Mini-CRM full stack em Django com board Kanban para gestão de tarefas
> vinculadas a contatos/clientes, API REST via Django REST Framework e
> painel administrativo integrado. Projeto demonstra modelagem de dados
> relacional, CRUD completo e construção de interface interativa com
> templates server-side — ideal para sistemas internos de gestão sob
> medida.
