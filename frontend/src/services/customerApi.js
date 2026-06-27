import axiosClient from './axiosClient';

export const getCustomers = async (params = {}) => axiosClient.get('/api/customers/', { params });
export const getCustomerDetail = async (customerId) => axiosClient.get(`/api/customers/${customerId}`);
export const createCustomer = async (payload) => axiosClient.post('/api/customers/', payload);
export const updateCustomer = async (customerId, payload) => axiosClient.put(`/api/customers/${customerId}`, payload);
export const updateChurnStatus = async (customerId, payload) => axiosClient.patch(`/api/customers/${customerId}/churn`, payload);
