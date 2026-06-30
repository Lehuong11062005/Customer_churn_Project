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
  payment_method: 'Electronic check', // Dùng đúng chuẩn text của dataset
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
    const { name, value } = e.target;
    
    // Ép kiểu tự động sang số (number) đối với các trường dạng số
    let parsedValue = value;
    if (['tenure_months', 'monthly_charges', 'total_charges'].includes(name)) {
      parsedValue = value === '' ? '' : Number(value);
    } else if (name === 'senior_citizen') {
      parsedValue = Number(value);
    }

    setForm({ ...form, [name]: parsedValue });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createCustomer(form);
      navigate('/customers');
    } catch (error) {
      console.error('Failed to create customer:', error);
      alert('Có lỗi xảy ra, vui lòng kiểm tra lại các trường dữ liệu!');
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-semibold mb-6">Create New Customer</h1>
      <form onSubmit={handleSubmit} className="space-y-6 rounded-xl bg-white p-8 shadow-md">
        
        {/* Nhóm 1: Định danh & Thông tin cá nhân */}
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Customer ID (*)</label>
            <input 
              className="w-full rounded border px-3 py-2" 
              name="customer_id" 
              required
              value={form.customer_id} 
              onChange={handleChange} 
              placeholder="VD: cs123"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Gender</label>
            <select className="w-full rounded border px-3 py-2" name="gender" value={form.gender} onChange={handleChange}>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Senior Citizen</label>
            <select className="w-full rounded border px-3 py-2" name="senior_citizen" value={form.senior_citizen} onChange={handleChange}>
              <option value={0}>No</option>
              <option value={1}>Yes</option>
            </select>
          </div>
        </div>

        {/* Nhóm 2: Thông tin gia đình & Hợp đồng */}
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Partner</label>
            <select className="w-full rounded border px-3 py-2" name="partner" value={form.partner} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Dependents</label>
            <select className="w-full rounded border px-3 py-2" name="dependents" value={form.dependents} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Contract Type</label>
            <select className="w-full rounded border px-3 py-2" name="contract" value={form.contract} onChange={handleChange}>
              <option value="Month-to-month">Month-to-month</option>
              <option value="One year">One year</option>
              <option value="Two year">Two year</option>
            </select>
          </div>
        </div>

        {/* Nhóm 3: Dịch vụ & Internet */}
        <div className="grid gap-4 md:grid-cols-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Phone Service</label>
            <select className="w-full rounded border px-3 py-2" name="phone_service" value={form.phone_service} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Multiple Lines</label>
            <select className="w-full rounded border px-3 py-2" name="multiple_lines" value={form.multiple_lines} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Internet Service</label>
            <select className="w-full rounded border px-3 py-2" name="internet_service" value={form.internet_service} onChange={handleChange}>
              <option value="DSL">DSL</option>
              <option value="Fiber optic">Fiber optic</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Paperless Billing</label>
            <select className="w-full rounded border px-3 py-2" name="paperless_billing" value={form.paperless_billing} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
        </div>

        {/* Nhóm 4: Các tính năng phụ trợ (Add-ons) */}
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Online Security</label>
            <select className="w-full rounded border px-3 py-2" name="online_security" value={form.online_security} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Online Backup</label>
            <select className="w-full rounded border px-3 py-2" name="online_backup" value={form.online_backup} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Device Protection</label>
            <select className="w-full rounded border px-3 py-2" name="device_protection" value={form.device_protection} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Tech Support</label>
            <select className="w-full rounded border px-3 py-2" name="tech_support" value={form.tech_support} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Streaming TV</label>
            <select className="w-full rounded border px-3 py-2" name="streaming_tv" value={form.streaming_tv} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Streaming Movies</label>
            <select className="w-full rounded border px-3 py-2" name="streaming_movies" value={form.streaming_movies} onChange={handleChange}>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
        </div>

        {/* Nhóm 5: Thanh toán & Cước phí */}
        <div className="grid gap-4 md:grid-cols-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Payment Method</label>
            <select className="w-full rounded border px-3 py-2" name="payment_method" value={form.payment_method} onChange={handleChange}>
              <option value="Electronic check">Electronic check</option>
              <option value="Mailed check">Mailed check</option>
              <option value="Credit card (automatic)">Credit card (automatic)</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Tenure Months</label>
            <input 
              type="number" 
              className="w-full rounded border px-3 py-2" 
              name="tenure_months" 
              value={form.tenure_months} 
              onChange={handleChange} 
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Monthly Charges</label>
            <input 
              type="number" 
              step="0.01" 
              className="w-full rounded border px-3 py-2" 
              name="monthly_charges" 
              value={form.monthly_charges} 
              onChange={handleChange} 
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Total Charges</label>
            <input 
              type="number" 
              step="0.01" 
              className="w-full rounded border px-3 py-2" 
              name="total_charges" 
              value={form.total_charges} 
              onChange={handleChange} 
            />
          </div>
        </div>

        {/* Nhóm 6: Địa lý (Tùy chọn thu gọn) */}
        <div className="grid gap-4 md:grid-cols-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">City</label>
            <input className="w-full rounded border px-3 py-2" name="city" value={form.city} onChange={handleChange} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">State</label>
            <input className="w-full rounded border px-3 py-2" name="state" value={form.state} onChange={handleChange} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Zip Code</label>
            <input className="w-full rounded border px-3 py-2" name="zip_code" value={form.zip_code} onChange={handleChange} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Country</label>
            <input className="w-full rounded border px-3 py-2" name="country" value={form.country} onChange={handleChange} />
          </div>
        </div>

        <div className="flex justify-end space-x-4 pt-4 border-t">
          <button 
            type="button" 
            onClick={() => navigate('/customers')}
            className="rounded bg-gray-300 px-6 py-2 text-gray-700 hover:bg-gray-400 font-medium transition"
          >
            Cancel
          </button>
          <button 
            className="rounded bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 font-medium transition" 
            type="submit"
          >
            Save Customer
          </button>
        </div>
      </form>
    </div>
  );
}