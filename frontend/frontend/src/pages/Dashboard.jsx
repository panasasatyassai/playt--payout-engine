import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { getDashboard, createPayout } from "../services/api";
import TransactionsTable from "../components/TransactionsTable";
import PayoutTable from "../components/PayoutTable";
import { useParams } from "react-router-dom";
import SimulatePayment from "../components/SimulatePayment";
import Loader from "../components/Loader";
import SkeletonCard from "../components/SkeletonCard";
import { getClientPayments } from "../services/api";

export default function Dashboard() {
  const { id } = useParams();
  const merchantId = id;

  const [data, setData] = useState(null);
  const [amount, setAmount] = useState("");
  const [idempotencyKey, setIdempotencyKey] = useState(null);
  const [loading, setLoading] = useState(false);
  const [clientPayments, setClientPayments] = useState(0);

  // ==========================
  // 🔥 Load Dashboard Data
  // ==========================
  const loadData = async () => {
    try {
      const res = await getDashboard(merchantId);

      console.log("Dashboard Data:", res);

      setData(res); // ✅ now res = data.data
    } catch (err) {
      console.error("Dashboard error:", err);
      toast.error("Failed to load dashboard");
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(() => {
        console.log("🔄 Auto refreshing...");
        loadData();
    }, 5000); // every 5 seconds

    return () => clearInterval(interval);
  }, [merchantId]);

  // ==========================
  // 🔥 Withdraw Handler (FINAL)
  // ==========================
  const handleWithdraw = async () => {
    if (!amount) {
      return toast.error("Please enter amount");
    }

    try {
      setLoading(true);

      let key = idempotencyKey;

      // ✅ Generate key ONLY once
      if (!key) {
        key = crypto.randomUUID();
        setIdempotencyKey(key);
      }

      const res = await createPayout(
        merchantId,
        Number(amount),
        key
      );

      console.log("Payout response:", res);

      // ✅ Reset after success (important)
      setIdempotencyKey(null);
      setAmount("");

      // 🔄 Refresh dashboard
      loadData();

    } catch (err) {
      console.error("Withdraw error:", err);
      setAmount("");
      toast.error(err.message || "Withdraw failed");
    } finally {
      setLoading(false);
    }
  };

  // ==========================
  // ⏳ Loading UI
  // ==========================
  if (!data) {
    return (
      <div className="p-6 grid md:grid-cols-3 gap-6">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }


  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {loading && <Loader />}

      {/* Header */}
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        👤 {data.merchant.name} Dashboard
      </h1>

      {/* Cards */}
      <div className="grid md:grid-cols-3 gap-6 mb-6">

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">Available Balance</p>
          <h2 className="text-2xl font-bold text-green-600">
            ₹{data.ledger_balance}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">Total Credit</p>
          <h2 className="text-green-600 font-bold">
            ₹{data.total_credit}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">Total Debit</p>
          <h2 className="text-red-600 font-bold">
            ₹{data.total_debit}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
        <p className="text-gray-500">Client Payments</p>
        <h2 className="text-blue-600 font-bold text-2xl">
            ₹{data.client_payments}
        </h2>
        </div>
         {/* 🔥 Held Balance */}
      <div className="bg-white p-6 rounded-xl shadow">
        <p className="text-gray-500">Held Balance</p>
        <h2 className="text-yellow-600 font-bold text-2xl">
          ₹{data.held_balance}
        </h2>
      </div>

      </div>

      {/* 💰 Simulate Client Payment */}
      <SimulatePayment merchantId={merchantId} refresh={loadData} />

      {/* Withdraw Section */}
      <div className="bg-white p-6 rounded-xl shadow mb-6">
        <h2 className="font-semibold mb-3">Withdraw Money</h2>

        <div className="flex gap-3">

          <input
            type="number"
            placeholder="Enter amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="border p-3 rounded w-full"
          />

          <button
            onClick={handleWithdraw}
            disabled={loading}
            className={`px-6 rounded text-white ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Processing..." : "Withdraw"}
          </button>

        </div>
      </div>

      {/* Tables */}
      <TransactionsTable transactions={data.recent_transactions || []} />
      <PayoutTable payouts={data.payouts || []} />

    </div>
  );
}