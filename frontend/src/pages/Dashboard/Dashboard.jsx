import { useEffect, useState } from 'react';
import { ResponsiveContainer, BarChart, Bar, CartesianGrid, Legend, Tooltip, XAxis, YAxis } from 'recharts';
import { getDashboardSummary, getChurnByContract } from '../../services/dashboardApi';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [summaryRes, chartRes] = await Promise.all([
          getDashboardSummary(),
          getChurnByContract(),
        ]);
        setSummary(summaryRes.data);
        setChartData(chartRes.data);
      } catch (error) {
        console.error('Failed to load dashboard:', error);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return <div className="p-6 text-center">Loading dashboard...</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-semibold mb-8">Dashboard</h1>
      
      {summary ? (
        <div className="grid gap-4 md:grid-cols-4 mb-8">
          <div className="rounded-xl bg-white p-6 shadow hover:shadow-lg transition">
            <p className="text-sm text-gray-600 mb-2">Total Customers</p>
            <p className="text-3xl font-bold text-blue-600">{summary.total_customers}</p>
          </div>
          <div className="rounded-xl bg-white p-6 shadow hover:shadow-lg transition">
            <p className="text-sm text-gray-600 mb-2">Current Churn Rate</p>
            <p className="text-3xl font-bold text-orange-600">{(summary.current_churn_rate * 100).toFixed(2)}%</p>
          </div>
          <div className="rounded-xl bg-white p-6 shadow hover:shadow-lg transition">
            <p className="text-sm text-gray-600 mb-2">High Risk Count</p>
            <p className="text-3xl font-bold text-red-600">{summary.high_risk_count}</p>
          </div>
          <div className="rounded-xl bg-white p-6 shadow hover:shadow-lg transition">
            <p className="text-sm text-gray-600 mb-2">Total Revenue</p>
            <p className="text-3xl font-bold text-green-600">${summary.total_revenue.toLocaleString()}</p>
          </div>
        </div>
      ) : null}

      <div className="rounded-xl bg-white p-6 shadow">
        <h2 className="text-xl font-semibold mb-4">Churn by Contract Type</h2>
        {chartData.length > 0 ? (
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
        ) : (
          <p className="text-gray-600">No chart data available</p>
        )}
      </div>
    </div>
  );
}
