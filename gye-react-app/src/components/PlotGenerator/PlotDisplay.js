export function PlotDisplay({ plot, error }) {
  if (error) {
    return <div className="text-red-600 text-sm mt-2">{error}</div>;
  }

  if (!plot) {
    return null;
  }

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">Generated Plot:</h3>
      <div className="bg-gray-50 rounded-md p-4">{plot}</div>
    </div>
  );
}
