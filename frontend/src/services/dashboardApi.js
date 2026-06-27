import axiosClient from './axiosClient';

export const getDashboardSummary = async () => axiosClient.get('/api/dashboard/summary');
export const getChurnByContract = async () => axiosClient.get('/api/dashboard/charts/churn-by-contract');
