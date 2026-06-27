import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getCustomers } from '../../services/customerApi';

export default function CustomerList() {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    const load = async () => {
      const response = await getCustomers({ page: 1, limit: 10 });
      setCustomers(response.data.data);
    };
    load();
  }, []);

  return (
    <div className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Customers</h1>
        <Link to="/customers/new" className="rounded bg-blue-600 px-4 py-2 text-white">New Customer</Link>
      </div>
      <div className="overflow-x-auto rounded-xl bg-white shadow">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100">
            <tr>
              <th className="px-4 py-2 text-left">Customer ID</th>
              <th className="px-4 py-2 text-left">City</th>
              <th className="px-4 py-2 text-left">Contract</th>
              <th className="px-4 py-2 text-left">Churn Score</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id} className="border-t">
                <td className="px-4 py-2"><Link to={`/customers/${customer.customer_id}`} className="text-blue-600">{customer.customer_id}</Link></td>
                <td className="px-4 py-2">{customer.city}</td>
                <td className="px-4 py-2">{customer.contract}</td>
                <td className="px-4 py-2">{customer.churn_score ?? 'n/a'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
