import { useNavigate } from "react-router-dom";

export default function MerchantList({ merchants }) {
  const navigate = useNavigate();

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-3">Merchants</h2>

      {merchants.map((m) => (
        <div
          key={m.id}
          onClick={() => navigate(`/dashboard/${m.id}`)} // 🔥 IMPORTANT
          className="bg-white p-4 mb-2 shadow rounded cursor-pointer hover:bg-gray-100"
        >
          {m.name}
        </div>
      ))}
    </div>
  );
}