import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getMenuItems = () => {
    const baseItems = [
      { label: 'Dashboard', path: '/', icon: '📊' },
      { label: 'Customers', path: '/customers', icon: '👥' },
      { label: 'Model Performance', path: '/model-performance', icon: '🤖' },
    ];

    if (user?.role === 'admin' || user?.role === 'manager') {
      baseItems.push({ label: 'Users', path: '/users', icon: '👤' });
    }

    return baseItems;
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 text-white shadow-lg">
        <div className="p-6 border-b border-slate-700">
          <h1 className="text-xl font-bold">Telco CRM</h1>
        </div>

        <nav className="flex-1 p-6">
          <div className="space-y-2 mb-8">
            {getMenuItems().map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="block rounded px-4 py-2 hover:bg-slate-700 transition"
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </div>
        </nav>

        {user && (
          <div className="border-t border-slate-700 p-6">
            <p className="text-xs text-slate-400 mb-3">Logged in as</p>
            <p className="font-semibold text-sm mb-1">{user.username}</p>
            <p className="text-xs text-slate-400 mb-4 capitalize">{user.role}</p>
            <div className="space-y-2">
              <Link to="/profile" className="block rounded px-4 py-2 hover:bg-slate-700 transition text-sm">
                🔐 Profile
              </Link>
              <Link to="/change-password" className="block rounded px-4 py-2 hover:bg-slate-700 transition text-sm">
                🔑 Change Password
              </Link>
              <button
                onClick={handleLogout}
                className="w-full text-left rounded px-4 py-2 hover:bg-red-700 transition text-sm"
              >
                🚪 Logout
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1">
        <main className="bg-slate-50 min-h-screen">
          {children}
        </main>
      </div>
    </div>
  );
}
