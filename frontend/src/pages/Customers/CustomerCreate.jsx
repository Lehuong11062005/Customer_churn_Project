import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createCustomer } from '../../services/customerApi';

const initialState = {
  customer_id: '',
  gender: 'Male',
  senior_citizen: 0,
  partner: 'Yes',
  dependents: 'No',
  tenure_months: 12,
  phone_service: 'Yes',
  multiple_lines: 'No',
  internet_service: 'DSL',
  online_security: 'No',
  online_backup: 'No',
  device_protection: 'No',
  tech_support: 'No',
  streaming_tv: 'No',
  streaming_movies: 'No',
  contract: 'Month-to-month',
  paperless_billing: 'Yes',
  payment_method: 'Credit card',
  monthly_charges: 50,
  total_charges: 600,
  city: 'Unknown',
  state: 'Unknown',
  zip_code: '00000',
  country: 'US',
};

export default function CustomerCreate() {
  const [form, setForm] = useState(initialState);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createCustomer(form);
    navigate('/customers');
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Create Customer</h1>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-xl bg-white p-6 shadow">
        <div className="grid gap-4 md:grid-cols-2">
          {Object.entries(initialState).map(([key, value]) => (
            <div key={key}>
              <label className="mb-1 block text-sm font-medium">{key}</label>
              <input className="w-full rounded border px-3 py-2" name={key} value={form[key]} onChange={handleChange} />
            </div>
          ))}
        </div>
        <button className="rounded bg-blue-600 px-4 py-2 text-white" type="submit">Save</button>
      </form>
    </div>
  );
}
