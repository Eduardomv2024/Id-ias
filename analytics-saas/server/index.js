/**
 * Analytics SaaS — backend
 * Express + JWT auth + API REST de métricas (dados mockados de forma
 * determinística para a demo).
 */
import express from "express";
import cors from "cors";
import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";

const app = express();
const PORT = process.env.PORT || 4000;
const JWT_SECRET = "dev-secret-change-in-production";

app.use(cors());
app.use(express.json());

// ------------------------------------------------------------- "DATABASE"
const users = [
  {
    id: 1,
    name: "Demo",
    email: "demo@saas.com",
    // senha: demo1234
    passwordHash: bcrypt.hashSync("demo1234", 8),
  },
];

// -------------------------------------------------------------- HELPERS
function seededRandom(seed) {
  let s = seed % 2147483647;
  if (s <= 0) s += 2147483646;
  return () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

function buildMetrics() {
  const rand = seededRandom(42);
  const months = ["Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago"];
  let revenue = 8000;
  let users_ = 120;
  const revenueSeries = months.map((month) => {
    revenue = revenue * (1 + (rand() * 0.18 + 0.02));
    return { month, revenue: Math.round(revenue) };
  });
  const usersSeries = months.map((month) => {
    users_ = Math.round(users_ * (1 + (rand() * 0.14 + 0.03)));
    return { month, users: users_ };
  });
  const categories = [
    { name: "Assinaturas", value: 45 },
    { name: "Consultoria", value: 25 },
    { name: "Add-ons", value: 18 },
    { name: "Parcerias", value: 12 },
  ];
  const churnSeries = months.map((month) => ({
    month,
    churn: +(rand() * 3 + 1.5).toFixed(1),
  }));

  return {
    kpis: {
      mrr: revenueSeries[revenueSeries.length - 1].revenue,
      activeUsers: usersSeries[usersSeries.length - 1].users,
      churnRate: churnSeries[churnSeries.length - 1].churn,
      conversionRate: 3.8,
    },
    revenueSeries,
    usersSeries,
    categories,
    churnSeries,
  };
}

const METRICS = buildMetrics();

// -------------------------------------------------------------- MIDDLEWARE
function authRequired(req, res, next) {
  const header = req.headers.authorization || "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : null;
  if (!token) return res.status(401).json({ error: "Token ausente" });
  try {
    req.user = jwt.verify(token, JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: "Token inválido ou expirado" });
  }
}

// -------------------------------------------------------------- ROUTES
app.get("/api/health", (req, res) => res.json({ ok: true }));

app.post("/api/auth/register", (req, res) => {
  const { name, email, password } = req.body || {};
  if (!name || !email || !password) {
    return res.status(400).json({ error: "Preencha nome, e-mail e senha" });
  }
  if (users.find((u) => u.email === email)) {
    return res.status(409).json({ error: "E-mail já cadastrado" });
  }
  const user = { id: users.length + 1, name, email, passwordHash: bcrypt.hashSync(password, 8) };
  users.push(user);
  const token = jwt.sign({ id: user.id, name: user.name, email: user.email }, JWT_SECRET, { expiresIn: "8h" });
  res.status(201).json({ token, user: { id: user.id, name: user.name, email: user.email } });
});

app.post("/api/auth/login", (req, res) => {
  const { email, password } = req.body || {};
  const user = users.find((u) => u.email === email);
  if (!user || !bcrypt.compareSync(password || "", user.passwordHash)) {
    return res.status(401).json({ error: "E-mail ou senha inválidos" });
  }
  const token = jwt.sign({ id: user.id, name: user.name, email: user.email }, JWT_SECRET, { expiresIn: "8h" });
  res.json({ token, user: { id: user.id, name: user.name, email: user.email } });
});

app.get("/api/metrics", authRequired, (req, res) => {
  res.json(METRICS);
});

app.get("/api/me", authRequired, (req, res) => {
  res.json({ user: req.user });
});

app.listen(PORT, () => {
  console.log(`Analytics SaaS API rodando em http://localhost:${PORT}`);
  console.log(`Usuário demo: demo@saas.com / demo1234`);
});
