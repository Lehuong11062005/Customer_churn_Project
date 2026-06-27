import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createUser } from '../../services/userApi';

export default function UserCreate() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    full_name: '',
    password: '',
    role: 'staff',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!form.username || !form.email || !form.password) {
      setError('Username, email, and password are required');
      return;
    }

    if (form.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    try {
      await createUser(form);
      setSuccess('User created successfully');
      setTimeout(() => navigate('/users'), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create user');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Create New User</h1>
      <form onSubmit={handleSubmit} className="max-w-md rounded-xl bg-white p-6 shadow">
        {error && <p className="mb-4 text-sm text-red-600 bg-red-50 p-3 rounded">{error}</p>}
        {success && <p className="mb-4 text-sm text-green-600 bg-green-50 p-3 rounded">{success}</p>}

        <div className="mb-4">
          <label className="mb-2 block text-sm font-medium">Username</label>
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            className="w-full rounded border px-3 py-2"
            placeholder="Enter username"
          />
        </div>

        <div className="mb-4">
          <label className="mb-2 block text-sm font-medium">Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            className="w-full rounded border px-3 py-2"
            placeholder="Enter email"
          />
        </div>

        <div className="mb-4">
          <label className="mb-2 block text-sm font-medium">Full Name</label>
          <input
            type="text"
            name="full_name"
            value={form.full_name}
            onChange={handleChange}
            className="w-full rounded border px-3 py-2"
            placeholder="Enter full name"
          />
        </div>

        <div className="mb-4">
          <label className="mb-2 block text-sm font-medium">Password</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            className="w-full rounded border px-3 py-2"
            placeholder="Enter password"
          />
        </div>

        <div className="mb-6">
          <label className="mb-2 block text-sm font-medium">Role</label>
          <select name="role" value={form.role} onChange={handleChange} className="w-full rounded border px-3 py-2">
            <option value="staff">Staff</option>
            <option value="manager">Manager</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <button type="submit" className="w-full rounded bg-blue-600 px-4 py-2 text-white font-semibold hover:bg-blue-700">
          Create User
        </button>
      </form>
    </div>
  );
}
