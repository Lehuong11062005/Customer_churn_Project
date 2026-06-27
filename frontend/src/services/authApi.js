import axiosClient from './axiosClient';

export const login = async (payload) => axiosClient.post('/api/auth/login', payload);
export const getMe = async () => axiosClient.get('/api/auth/me');
