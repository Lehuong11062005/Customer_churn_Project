import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getCustomerDetail, updateChurnStatus } from "../../services/customerApi";
import { evaluatePrediction } from "../../services/predictApi";

export default function CustomerDetail() {
  const { customerId } = useParams();
  const [customer, setCustomer] = useState(null);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    const load = async () => {
      const response = await getCustomerDetail(customerId);
      setCustomer(response.data);

      const predictionResponse = await evaluatePrediction({
        data: response.data,
      });

      setPrediction(predictionResponse.data);
    };

    load();
  }, [customerId]);

  const markChurn = async () => {
    try {
      await updateChurnStatus(customerId, {
        churn_label: "Yes",
        churn_reason: "Customer requested cancellation",
      });

      const response = await getCustomerDetail(customerId);
      setCustomer(response.data);
    } catch (error) {
      console.log(error);
      alert("Không thể cập nhật.");
    }
  };

  if (!customer)
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-xl font-semibold">Loading...</div>
      </div>
    );

  const probability = prediction
    ? Number(prediction.churn_probability) * 100
    : 0;

  const riskColor =
    prediction?.risk_level === "High"
      ? "text-red-600 bg-red-100"
      : prediction?.risk_level === "Medium"
      ? "text-yellow-600 bg-yellow-100"
      : "text-green-600 bg-green-100";

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="mx-auto max-w-6xl">

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">
              Customer Detail
            </h1>
            <p className="text-gray-500">
              Customer ID: {customer.customer_id}
            </p>
          </div>

          {customer.churn_label === "Yes" ? (
            <span className="rounded-full bg-red-100 px-4 py-2 font-semibold text-red-600">
              🔴 Churned
            </span>
          ) : (
            <span className="rounded-full bg-green-100 px-4 py-2 font-semibold text-green-600">
              🟢 Active
            </span>
          )}
        </div>

        <div className="grid gap-6 lg:grid-cols-2">

          {/* Customer Info */}
          <div className="rounded-2xl bg-white p-6 shadow-lg">
            <h2 className="mb-5 text-xl font-bold text-gray-700">
              Customer Information
            </h2>

            <div className="space-y-4">

              <div className="flex justify-between border-b pb-2">
                <span className="text-gray-500">City</span>
                <span className="font-semibold">{customer.city}</span>
              </div>

              <div className="flex justify-between border-b pb-2">
                <span className="text-gray-500">Contract</span>
                <span className="font-semibold">{customer.contract}</span>
              </div>

              <div className="flex justify-between border-b pb-2">
                <span className="text-gray-500">Monthly Charges</span>
                <span className="font-semibold">
                  ${customer.monthly_charges}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-500">Churn Score</span>
                <span className="font-bold text-blue-600">
                  {customer.churn_score ?? "N/A"}
                </span>
              </div>
            </div>
          </div>

          {/* Prediction */}
          <div className="rounded-2xl bg-white p-6 shadow-lg">
            <h2 className="mb-5 text-xl font-bold text-gray-700">
              AI Prediction
            </h2>

            {prediction && (
              <>
                <div className="mb-5">
                  <div className="mb-2 flex justify-between">
                    <span className="font-medium text-gray-600">
                      Churn Probability
                    </span>
                    <span className="font-bold">
                      {probability.toFixed(1)}%
                    </span>
                  </div>

                  <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                    <div
                      className="h-full rounded-full bg-red-500"
                      style={{
                        width: `${probability}%`,
                      }}
                    />
                  </div>
                </div>

                <div className="space-y-4">

                  <div className="flex justify-between">
                    <span>Prediction</span>
                    <span
                      className={`font-bold ${
                        prediction.churn_prediction === "Yes"
                          ? "text-red-600"
                          : "text-green-600"
                      }`}
                    >
                      {prediction.churn_prediction}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span>Risk Level</span>

                    <span
                      className={`rounded-full px-3 py-1 text-sm font-semibold ${riskColor}`}
                    >
                      {prediction.risk_level}
                    </span>
                  </div>
                </div>
              </>
            )}

            <div className="mt-8">

              {customer.churn_label === "Yes" ? (
                <div className="rounded-lg bg-red-100 p-4 text-center font-semibold text-red-600">
                  🚨 This customer has already churned.
                </div>
              ) : (
                <button
                  onClick={markChurn}
                  className="w-full rounded-xl bg-red-600 py-3 text-lg font-semibold text-white transition hover:bg-red-700 active:scale-95"
                >
                  Mark as Churn
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}