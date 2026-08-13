import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth.jsx";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("demo@saas.com");
  const [password, setPassword] = useState("demo1234");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="auth-screen">
      <form className="auth-card" onSubmit={handleSubmit}>
        <div className="auth-logo">
          Pulse<span>Analytics</span>
        </div>
        <p className="auth-sub">Entre para ver o seu dashboard</p>

        {error && <div className="auth-error">{error}</div>}

        <label>E-mail</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />

        <label>Senha</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />

        <button className="btn btn-block" disabled={busy}>
          {busy ? "Entrando..." : "Entrar"}
        </button>

        <p className="auth-hint">Use a conta demo: demo@saas.com / demo1234</p>
        <p className="auth-switch">
          Não tem conta? <Link to="/register">Criar conta</Link>
        </p>
      </form>
    </div>
  );
}
