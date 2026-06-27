import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getUsers, updateUserStatus } from '../../services/userApi';
import { useAuth } from '../../context/AuthContext';

export default function UserList() {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState('');

  useEffect(() => {
    const loadUsers = async () => {
      try {
        setLoading(true);
        const params = { page, limit: 10 };
        if (roleFilter) params.role = roleFilter;
        const response = await getUsers(params);
        setUsers(response.data.data);
        setTotal(response.data.total);
      } catch (error) {
        console.error('Failed to load users:', error);
      } finally {
        setLoading(false);
      }
    };
    loadUsers();
  }, [page, roleFilter]);

  const handleToggleStatus = async (userId, currentStatus) => {
    try {
      await updateUserStatus(userId, !currentStatus);
      const response = await getUsers({ page, limit: 10, role: roleFilter });
      setUsers(response.data.data);
    } catch (error) {
      console.error('Failed to update user status:', error);
    }
  };

  const getRoleBadgeColor = (role) => {
    const colors = {
      admin: 'bg-red-100 text-red-800',
      manager: 'bg-blue-100 text-blue-800',
      staff: 'bg-green-100 text-green-800',
    };
    return colors[role] || 'bg-gray-100 text-gray-800';
  };

  const totalPages = Math.ceil(total / 10);

  if (loading) {
    return <div className="p-6 text-center">Loading users...</div>;
  }

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">User Management</h1>
        {user?.role === 'admin' && (
          <Link to="/users/new" className="rounded bg-blue-600 px-4 py-2 text-white font-semibold hover:bg-blue-700">
            New User
          </Link>
        )}
      </div>

      <div className="mb-6 flex gap-4">
        <select
          value={roleFilter}
          onChange={(e) => {
            setRoleFilter(e.target.value);
            setPage(1);
          }}
          className="rounded border px-3 py-2"
        >
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="manager">Manager</option>
          <option value="staff">Staff</option>
        </select>
      </div>

      <div className="overflow-x-auto rounded-xl bg-white shadow">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 border-b">
            <tr>
              <th className="px-4 py-3 text-left font-semibold">Username</th>
              <th className="px-4 py-3 text-left font-semibold">Email</th>
              <th className="px-4 py-3 text-left font-semibold">Full Name</th>
              <th className="px-4 py-3 text-left font-semibold">Role</th>
              <th className="px-4 py-3 text-left font-semibold">Status</th>
              {user?.role === 'admin' && (
                <th className="px-4 py-3 text-left font-semibold">Actions</th>
              )}
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-t hover:bg-slate-50">
                <td className="px-4 py-3">{u.username}</td>
                <td className="px-4 py-3">{u.email}</td>
                <td className="px-4 py-3">{u.full_name || '-'}</td>
                <td className="px-4 py-3">
                  <span className={`inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRoleBadgeColor(u.role)}`}>
                    {u.role}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className={`inline-block px-3 py-1 rounded text-xs font-semibold ${u.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {u.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                {user?.role === 'admin' && (
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleToggleStatus(u.id, u.is_active)}
                      className={`rounded px-3 py-1 text-xs font-semibold text-white ${u.is_active ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}`}
                    >
                      {u.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 flex items-center justify-between">
        <p className="text-sm text-gray-600">
          Showing {users.length} of {total} users
        </p>
        <div className="flex gap-2">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="rounded border px-3 py-2 disabled:opacity-50"
          >
            Previous
          </button>
          <span className="px-3 py-2">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="rounded border px-3 py-2 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
