import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../../services/authApi';
import { useAuth } from '../../context/AuthContext';

export default function Login() {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { setToken, setUser } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await login(form);
      setToken(response.data.access_token);
      setUser(response.data.user);
      navigate('/');
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg">
        <h1 className="text-2xl font-semibold mb-6">Telco CRM Login</h1>
        {error ? <p className="mb-4 text-sm text-red-600">{error}</p> : null}
        <input className="mb-3 w-full rounded border px-3 py-2" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} placeholder="Username" />
        <input className="mb-3 w-full rounded border px-3 py-2" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="Password" />
        <button className="w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white" type="submit">Sign In</button>
      </form>
    </div>
  );
}
