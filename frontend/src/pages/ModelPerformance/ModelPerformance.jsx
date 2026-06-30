import { useEffect, useState } from "react";
import modelPerformanceApi from "../../services/modelPerformanceApi";

const MetricCard = ({ title, value, color }) => (
    <div className="bg-white rounded-xl shadow-md p-5 border-l-4" style={{ borderColor: color }}>
        <p className="text-sm text-gray-500">{title}</p>
        <h2 className="text-3xl font-bold mt-2" style={{ color }}>
            {value}
        </h2>
    </div>
);

const ModelPerformance = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchPerformance = async () => {
            try {
                const result = await modelPerformanceApi.getPerformance();
                setData(result);
            } catch (err) {
                console.error(err);
                setError("Unable to load model performance.");
            } finally {
                setLoading(false);
            }
        };

        fetchPerformance();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="text-xl font-semibold text-gray-600">
                    Loading Model Performance...
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-8">
                <div className="bg-red-100 text-red-700 p-4 rounded-lg">
                    {error}
                </div>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="p-8">
                <div className="bg-yellow-100 text-yellow-700 p-4 rounded-lg">
                    No model performance found.
                </div>
            </div>
        );
    }

    const cm = data.confusion_matrix;
    const model = data.model_information;

    return (
        <div className="p-8 bg-slate-50 min-h-screen">

            {/* Header */}

            <div className="mb-8">
                <h1 className="text-3xl font-bold text-slate-800">
                    Model Performance
                </h1>

                <p className="text-gray-500 mt-2">
                    Evaluate the performance of the Churn Prediction Random Forest model.
                </p>
            </div>

            {/* KPI */}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-5 mb-8">

                <MetricCard
                    title="Accuracy"
                    value={`${(data.accuracy * 100).toFixed(2)}%`}
                    color="#16a34a"
                />

                <MetricCard
                    title="Precision"
                    value={`${(data.precision * 100).toFixed(2)}%`}
                    color="#2563eb"
                />

                <MetricCard
                    title="Recall"
                    value={`${(data.recall * 100).toFixed(2)}%`}
                    color="#ea580c"
                />

                <MetricCard
                    title="F1 Score"
                    value={`${(data.f1_score * 100).toFixed(2)}%`}
                    color="#9333ea"
                />

                <MetricCard
                    title="OOB Score"
                    value={`${(data.oob_score * 100).toFixed(2)}%`}
                    color="#0891b2"
                />

            </div>

            {/* Model + Matrix */}

            <div className="grid lg:grid-cols-2 gap-6 mb-8">

                {/* Model */}

                <div className="bg-white rounded-xl shadow-md p-6">

                    <h2 className="text-xl font-bold mb-5">
                        Model Information
                    </h2>

                    <div className="space-y-3">

                        <div className="flex justify-between">
                            <span>Algorithm</span>
                            <span className="font-semibold">
                                {model.algorithm}
                            </span>
                        </div>

                        <div className="flex justify-between">
                            <span>Estimators</span>
                            <span>{model.n_estimators}</span>
                        </div>

                        <div className="flex justify-between">
                            <span>Max Depth</span>
                            <span>{model.max_depth}</span>
                        </div>

                        <div className="flex justify-between">
                            <span>Features</span>
                            <span>{model.feature_count}</span>
                        </div>

                        <div className="flex justify-between">
                            <span>Training Samples</span>
                            <span>{model.train_samples}</span>
                        </div>

                        <div className="flex justify-between">
                            <span>Testing Samples</span>
                            <span>{model.test_samples}</span>
                        </div>

                    </div>

                </div>

                {/* Confusion Matrix */}

                <div className="bg-white rounded-xl shadow-md p-6">

                    <h2 className="text-xl font-bold mb-5">
                        Confusion Matrix
                    </h2>

                    <table className="w-full border-collapse">

                        <thead>

                            <tr className="bg-slate-100">
                                <th className="border p-3"></th>
                                <th className="border p-3">Predicted No</th>
                                <th className="border p-3">Predicted Yes</th>
                            </tr>

                        </thead>

                        <tbody>

                            <tr>

                                <th className="border p-3 bg-slate-100">
                                    Actual No
                                </th>

                                <td className="border p-4 text-center bg-green-100 font-bold">
                                    {cm.true_negative}
                                </td>

                                <td className="border p-4 text-center bg-red-100 font-bold">
                                    {cm.false_positive}
                                </td>

                            </tr>

                            <tr>

                                <th className="border p-3 bg-slate-100">
                                    Actual Yes
                                </th>

                                <td className="border p-4 text-center bg-red-100 font-bold">
                                    {cm.false_negative}
                                </td>

                                <td className="border p-4 text-center bg-green-100 font-bold">
                                    {cm.true_positive}
                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

            {/* Feature Importance */}

            <div className="bg-white rounded-xl shadow-md p-6">

                <h2 className="text-xl font-bold mb-6">
                    Feature Importance
                </h2>

                <div className="overflow-x-auto">

                    <table className="min-w-full">

                        <thead>

                            <tr className="border-b bg-slate-100">

                                <th className="text-left p-3">
                                    Rank
                                </th>

                                <th className="text-left p-3">
                                    Feature
                                </th>

                                <th className="text-left p-3">
                                    Importance
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {data.feature_importance.map((item, index) => (

                                <tr
                                    key={item.feature}
                                    className="border-b hover:bg-slate-50"
                                >

                                    <td className="p-3 font-semibold">
                                        #{index + 1}
                                    </td>

                                    <td className="p-3">
                                        {item.feature}
                                    </td>

                                    <td className="p-3">

                                        <div className="flex items-center gap-4">

                                            <div className="w-full bg-gray-200 rounded-full h-3">

                                                <div
                                                    className="bg-blue-600 h-3 rounded-full"
                                                    style={{
                                                        width: `${item.importance * 100}%`
                                                    }}
                                                />

                                            </div>

                                            <span className="w-16 text-right font-semibold">
                                                {item.importance.toFixed(4)}
                                            </span>

                                        </div>

                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>
    );
};

export default ModelPerformance;