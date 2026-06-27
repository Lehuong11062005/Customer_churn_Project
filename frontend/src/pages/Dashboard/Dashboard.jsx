import { useEffect, useState } from 'react';
import { ResponsiveContainer, BarChart, Bar, CartesianGrid, Legend, Tooltip, XAxis, YAxis } from 'recharts';
import { getCustomers } from '../../services/customerApi';
import axiosClient from '../../services/axiosClient';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const load = async () => {
      const [summaryRes, chartRes] = await Promise.all([
        axiosClient.get('/api/dashboard/summary'),
        axiosClient.get('/api/dashboard/charts/churn-by-contract'),
      ]);
      setSummary(summaryRes.data);
      setChartData(chartRes.data);
    };
    load();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Dashboard</h1>
      {summary ? (
        <div className="grid gap-4 md:grid-cols-4 mb-8">
          <div className="rounded-xl bg-white p-4 shadow">Total Customers: {summary.total_customers}</div>
          <div className="rounded-xl bg-white p-4 shadow">Current Churn Rate: {summary.current_churn_rate}</div>
          <div className="rounded-xl bg-white p-4 shadow">High Risk Count: {summary.high_risk_count}</div>
          <div className="rounded-xl bg-white p-4 shadow">Total Revenue: {summary.total_revenue}</div>
        </div>
      ) : null}
      <div className="rounded-xl bg-white p-4 shadow">
        <h2 className="text-lg font-semibold mb-4">Churn by Contract</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="churned" fill="#ef4444" />
            <Bar dataKey="retained" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
