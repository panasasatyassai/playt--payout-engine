export default function TransactionsTable({ transactions = [] }) {
  return (
    <div className="bg-white p-4 shadow rounded mt-6">
      <h2 className="font-semibold mb-3">Transactions</h2>

      {transactions.length === 0 ? (
        <div className="text-center text-gray-500 py-6">
          No transactions yet 🚫
        </div>
      ) : (
        <table className="w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2">Type</th>
              <th className="p-2">Amount</th>
              <th className="p-2">Time</th>
            </tr>
          </thead>

          <tbody>
            {transactions.map((t, i) => (
              <tr key={i} className="text-center border-t">
                <td className={t.transaction_type === "credit" ? "text-green-600" : "text-red-600"}>
                  {t.transaction_type}
                </td>
                <td>₹{t.amount}</td>
                <td>{new Date(t.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}