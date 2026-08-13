# PulseAnalytics — Dashboard SaaS de Analytics

Mini-SaaS full stack com autenticação e dashboard de métricas de negócio,
no estilo de produtos como Mixpanel/Baremetrics.

**Stack:** Node.js, Express, JWT, React (Vite), Recharts.

## Funcionalidades

- Autenticação com registro/login e tokens JWT
- API REST protegida por middleware de autenticação
- Dashboard com KPIs (MRR, usuários ativos, conversão, churn)
- Gráficos interativos: receita mensal, receita por categoria,
  crescimento de usuários e churn mensal (Recharts)
- Layout responsivo

## Como rodar localmente

Backend:
```bash
cd analytics-saas/server
npm install
npm start                # inicia em http://localhost:4000
```

Frontend (em outro terminal):
```bash
cd analytics-saas/client
npm install
npm run dev               # inicia em http://localhost:5173
```

Conta de demonstração já cadastrada: **demo@saas.com** / **demo1234**
(ou crie uma conta nova pela tela de cadastro).

## Texto para o portfólio do Workana

> **PulseAnalytics — Dashboard SaaS de Analytics**
> Mini-SaaS full stack com autenticação (Node.js/Express + JWT) e dashboard
> interativo em React, exibindo métricas de negócio como receita
> recorrente, crescimento de usuários, churn e conversão. Projeto
> demonstra API REST protegida, gerenciamento de estado de autenticação no
> front-end e visualização de dados com gráficos (Recharts) — a base de
> qualquer produto SaaS com painel de métricas.
