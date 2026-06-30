import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { getMe } from '../services/authApi'; // Import API bạn vừa tạo ở Bước 1

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [loading, setLoading] = useState(true);

  // 1. Quản lý việc lưu token vào localStorage
  useEffect(() => {
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }, [token]);

  // 2. Tự động phục hồi thông tin User khi có token (ngay cả khi F5)
  useEffect(() => {
    const fetchUserProfile = async () => {
      if (token) {
        try {
          // Gọi API để lấy thông tin chi tiết (bao gồm cả role)
          const response = await getMe();
          
          // Data trả về từ /api/auth/me đã là một dict thuần túy
          setUser(response.data); 
        } catch (error) {
          console.error("Lỗi xác thực hoặc Token hết hạn:", error);
          logout(); // Tự động xóa token lỗi và đá về trang Login
        }
      }
      setLoading(false); // Xong xuôi thì tắt loading
    };

    fetchUserProfile();
  }, [token]);

  const logout = () => {
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, setUser, token, setToken, logout, loading }),
    [user, token, loading]
  );

  return (
    <AuthContext.Provider value={value}>
      {/* Chỉ render các màn hình bên trong khi đã tải xong dữ liệu user */}
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);