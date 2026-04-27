export default function PayoutTable({ payouts = [] }) {
  return (
    <div className="bg-white p-4 shadow rounded mt-6">
      <h2 className="font-semibold mb-3">Payout History</h2>

      {payouts.length === 0 ? (
        <div className="text-center text-gray-500 py-6">
          No payouts yet 💸
        </div>
      ) : (
        <table className="w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2">Amount</th>
              <th className="p-2">Status</th>
              <th className="p-2">Attempts</th>
              <th className="p-2">Time</th>
            </tr>
          </thead>

          <tbody>
            {payouts.map((p, i) => (
              <tr key={i} className="text-center border-t">
                <td>₹{p.amount_paise}</td>

                <td className={
                  p.status === "completed"
                    ? "text-green-600"
                    : p.status === "failed"
                    ? "text-red-600"
                    : "text-yellow-600"
                }>
                  {p.status}
                </td>

                <td>{p.attempts}</td>
                <td>{new Date(p.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}