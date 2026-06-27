import { useState } from 'react';
import { changePassword } from '../../services/userApi';

export default function ChangePassword() {
  const [form, setForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!form.currentPassword || !form.newPassword || !form.confirmPassword) {
      setError('All fields are required');
      return;
    }

    if (form.newPassword !== form.confirmPassword) {
      setError('New password and confirmation do not match');
      return;
    }

    if (form.newPassword.length < 6) {
      setError('New password must be at least 6 characters');
      return;
    }

    if (form.currentPassword === form.newPassword) {
      setError('New password must be different from current password');
      return;
    }

    try {
      await changePassword(form.currentPassword, form.newPassword);
      setSuccess('Password changed successfully');
      setForm({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to change password');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Change Password</h1>
      <form onSubmit={handleSubmit} className="max-w-md rounded-xl bg-white p-6 shadow">
        {error && <p className="mb-4 text-sm text-red-600 bg-red-50 p-3 rounded">{error}</p>}
        {success && <p className="mb-4 text-sm text-green-600 bg-green-50 p-3 rounded">{success}</p>}

        <div className="mb-4">
          <label className="mb-2 block text-sm font-medium">Current Password</label>
          <input
            type="password"
            name="currentPassword"
            value={form.currentPassword}
            onChange={handleChange}
            className="w-full rounded border px-3 py-2"
            placeholder="Enter current password"
          />
        </div>

        <div className="mb-4">
          <label className="mb-2 block text-sm font-medium">New Password</label>
          <input
            type="password"
            name="newPassword"
            value={form.newPassword}
            onChange={handleChange}
            className="w-full rounded border px-3 py-2"
            placeholder="Enter new password"
          />
        </div>

        <div className="mb-6">
          <label className="mb-2 block text-sm font-medium">Confirm New Password</label>
          <input
            type="password"
            name="confirmPassword"
            value={form.confirmPassword}
            onChange={handleChange}
            className="w-full rounded border px-3 py-2"
            placeholder="Confirm new password"
          />
        </div>

        <button type="submit" className="w-full rounded bg-blue-600 px-4 py-2 text-white font-semibold hover:bg-blue-700">
          Change Password
        </button>
      </form>
    </div>
  );
}
