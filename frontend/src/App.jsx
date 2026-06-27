import { Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ProtectedRoute, RoleRoute } from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Auth/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import CustomerList from './pages/Customers/CustomerList';
import CustomerCreate from './pages/Customers/CustomerCreate';
import CustomerDetail from './pages/Customers/CustomerDetail';
import UserList from './pages/Users/UserList';
import UserCreate from './pages/Users/UserCreate';
import Profile from './pages/Profile/Profile';
import ChangePassword from './pages/Profile/ChangePassword';
import NotFound from './pages/NotFound';
import Unauthorized from './pages/Unauthorized';

function AppRoutes() {
  const { token } = useAuth();

  if (!token) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/customers" element={<ProtectedRoute><CustomerList /></ProtectedRoute>} />
        <Route path="/customers/new" element={<ProtectedRoute><CustomerCreate /></ProtectedRoute>} />
        <Route path="/customers/:customerId" element={<ProtectedRoute><CustomerDetail /></ProtectedRoute>} />
        <Route path="/users" element={<RoleRoute allowedRoles={['admin', 'manager']}><UserList /></RoleRoute>} />
        <Route path="/users/new" element={<RoleRoute allowedRoles={['admin']}><UserCreate /></RoleRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/change-password" element={<ProtectedRoute><ChangePassword /></ProtectedRoute>} />
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
