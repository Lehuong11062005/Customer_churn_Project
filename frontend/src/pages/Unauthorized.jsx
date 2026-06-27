export default function Unauthorized() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="text-center rounded-xl bg-white p-8 shadow-lg max-w-md">
        <h1 className="text-4xl font-bold text-red-600 mb-4">403</h1>
        <p className="text-2xl font-semibold mb-2">Access Denied</p>
        <p className="text-gray-600 mb-6">You do not have permission to access this page.</p>
        <a href="/" className="inline-block rounded bg-blue-600 px-6 py-2 text-white font-semibold hover:bg-blue-700">
          Go to Dashboard
        </a>
      </div>
    </div>
  );
}
