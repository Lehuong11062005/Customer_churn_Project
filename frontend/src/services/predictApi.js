import axiosClient from './axiosClient';

export const evaluatePrediction = async (payload) => axiosClient.post('/api/predict/evaluate', payload);
