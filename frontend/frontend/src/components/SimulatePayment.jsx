import { useState } from "react";
import { simulatePayment } from "../services/api";

export default function SimulatePayment({ merchantId, refresh }) {
  const [amount, setAmount] = useState("");

  const handleSubmit = async () => {
    if (!amount) return alert("Enter amount");

    await simulatePayment(merchantId, Number(amount));

    setAmount("");
    refresh(); // reload dashboard
  };

  return (
    <div className="bg-white p-4 shadow rounded mt-6">
      <h2 className="font-semibold mb-3">💰 Simulate Client Payment</h2>

      <div className="flex gap-3">
        <input
          type="number"
          placeholder="Enter amount (paise)"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="border p-2 w-full rounded"
        />

        <button
          onClick={handleSubmit}
          className="bg-green-600 text-white px-4 rounded"
        >
          Add
        </button>
      </div>
    </div>
  );
}