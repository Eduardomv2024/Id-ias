import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { useAuth } from "../auth.jsx";

const COLORS = ["#7c3aed", "#38bdf8", "#fb923c", "#34d399"];
const currency = (v) => `R$ ${v.toLocaleString("pt-BR")}`;

export default function Dashboard() {
  const { user, token, logout, API_URL } = useAuth();
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/api/metrics`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then(setMetrics)
      .catch(() => setError("Não foi possível carregar as métricas."));
  }, [API_URL, token]);

  if (error) return <div className="dash-loading">{error}</div>;
  if (!metrics) return <div className="dash-loading">Carregando métricas…</div>;

  const { kpis, revenueSeries, usersSeries, categories, churnSeries } = metrics;

  return (
    <div className="dash">
      <header className="dash-topbar">
        <div className="dash-logo">
          Pulse<span>Analytics</span>
        </div>
        <div className="dash-user">
          <span>Olá, {user?.name || "usuário"}</span>
          <button className="btn btn-ghost" onClick={logout}>
            Sair
          </button>
        </div>
      </header>

      <main className="dash-content">
        <div className="kpi-grid">
          <div className="kpi-card">
            <p className="kpi-label">MRR (receita recorrente)</p>
            <p className="kpi-value">{currency(kpis.mrr)}</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">Usuários ativos</p>
            <p className="kpi-value">{kpis.activeUsers.toLocaleString("pt-BR")}</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">Taxa de conversão</p>
            <p className="kpi-value">{kpis.conversionRate}%</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">Churn</p>
            <p className="kpi-value warn">{kpis.churnRate}%</p>
          </div>
        </div>

        <div className="chart-grid">
          <div className="chart-card wide">
            <h3>Receita mensal (MRR)</h3>
            <ResponsiveContainer width="100%" height={260}>
              <AreaChart data={revenueSeries}>
                <defs>
                  <linearGradient id="rev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#7c3aed" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="#7c3aed" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip formatter={(v) => currency(v)} />
                <Area type="monotone" dataKey="revenue" stroke="#7c3aed" fill="url(#rev)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Receita por categoria</h3>
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={categories} dataKey="value" nameKey="name" innerRadius={55} outerRadius={85} paddingAngle={3}>
                  {categories.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Legend verticalAlign="bottom" height={36} />
                <Tooltip formatter={(v) => `${v}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Crescimento de usuários</h3>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={usersSeries}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="users" fill="#38bdf8" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card wide">
            <h3>Churn mensal</h3>
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={churnSeries}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} unit="%" />
                <Tooltip formatter={(v) => `${v}%`} />
                <Line type="monotone" dataKey="churn" stroke="#fb923c" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
}
