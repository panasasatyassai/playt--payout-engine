import { useState } from "react";
import { createPayout } from "../services/api";

export default function PayoutForm({ merchantId, refresh }) {
  const [amount, setAmount] = useState("");

  const handleWithdraw = async () => {
    if (!amount) return alert("Enter amount");

    const res = await createPayout(merchantId, Number(amount));

    if (res.error) {
      alert(res.error);
    } else {
      alert("Payout requested");
      setAmount("");
      refresh();
    }
  };

  return (
    <div className="bg-white p-4 shadow rounded mt-6">
      <h2 className="font-semibold mb-3">Withdraw Money</h2>

      <div className="flex gap-3">
        <input
          type="number"
          placeholder="Enter amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="border p-2 w-full rounded"
        />

        <button
          onClick={handleWithdraw}
          className="bg-blue-600 text-white px-4 rounded"
        >
          Withdraw
        </button>
      </div>
    </div>
  );
}