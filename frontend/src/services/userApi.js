import axiosClient from './axiosClient';

export const getUsers = async (params = {}) => axiosClient.get('/api/users/', { params });
export const getUserDetail = async (userId) => axiosClient.get(`/api/users/${userId}`);
export const createUser = async (payload) => axiosClient.post('/api/users/', payload);
export const updateUserStatus = async (userId, isActive) => axiosClient.patch(`/api/users/${userId}/status`, { is_active: isActive });
export const changePassword = async (oldPassword, newPassword) => axiosClient.put('/api/users/me/password', { old_password: oldPassword, new_password: newPassword });
