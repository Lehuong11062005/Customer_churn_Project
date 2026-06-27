import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getCustomerDetail, updateChurnStatus } from '../../services/customerApi';
import { evaluatePrediction } from '../../services/predictApi';

export default function CustomerDetail() {
  const { customerId } = useParams();
  const [customer, setCustomer] = useState(null);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    const load = async () => {
      const response = await getCustomerDetail(customerId);
      setCustomer(response.data);
      const predictionResponse = await evaluatePrediction({ data: response.data });
      setPrediction(predictionResponse.data);
    };
    load();
  }, [customerId]);

  const markChurn = async () => {
    await updateChurnStatus(customerId, { churn_label: 'Yes', churn_reason: 'Customer requested cancellation' });
    const response = await getCustomerDetail(customerId);
    setCustomer(response.data);
  };

  if (!customer) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Customer Detail</h1>
      <div className="grid gap-4 rounded-xl bg-white p-6 shadow md:grid-cols-2">
        <div>
          <p><strong>Customer ID:</strong> {customer.customer_id}</p>
          <p><strong>City:</strong> {customer.city}</p>
          <p><strong>Contract:</strong> {customer.contract}</p>
          <p><strong>Monthly Charges:</strong> {customer.monthly_charges}</p>
        </div>
        <div>
          <p><strong>Churn Score:</strong> {customer.churn_score ?? 'n/a'}</p>
          {prediction ? (
            <>
              <p><strong>Prediction:</strong> {prediction.churn_prediction}</p>
              <p><strong>Probability:</strong> {prediction.churn_probability}</p>
              <p><strong>Risk Level:</strong> {prediction.risk_level}</p>
            </>
          ) : null}
          <button className="mt-4 rounded bg-red-600 px-4 py-2 text-white" onClick={markChurn}>Mark Churn</button>
        </div>
      </div>
    </div>
  );
}
