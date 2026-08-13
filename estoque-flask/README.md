# EstoquePro — Sistema de Gestão de Estoque e Vendas

Mini-sistema full stack para controle de produtos, estoque e vendas, com
dashboard de indicadores em tempo real.

**Stack:** Python, Flask, SQLAlchemy, SQLite, Jinja2, CSS puro (sem
frameworks externos).

## Funcionalidades

- Dashboard com KPIs: produtos cadastrados, valor total em estoque, total
  vendido, alertas de estoque baixo e produtos mais vendidos
- CRUD completo de produtos (nome, SKU, categoria, preço, estoque mínimo)
- Registro de vendas com baixa automática de estoque
- Filtro de produtos por categoria
- Histórico de vendas

## Como rodar localmente

```bash
cd estoque-flask
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed.py                  # cria o banco e popula com dados de exemplo
python app.py                   # inicia em http://localhost:5000
```

## Texto para o portfólio do Workana

> **EstoquePro — Sistema de Gestão de Estoque e Vendas**
> Sistema full stack desenvolvido em Python (Flask + SQLAlchemy) para
> controle de produtos, estoque e vendas de pequenos e médios negócios.
> Conta com dashboard de indicadores (valor em estoque, vendas, alertas de
> estoque baixo), cadastro de produtos e registro de vendas com baixa
> automática de estoque. Projeto pensado para ser fácil de adaptar a
> diferentes segmentos — do varejo à prestação de serviços.
