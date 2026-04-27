export default function BalanceCard({ title, amount }) {
  return (
    <div className="bg-white shadow-md p-4 rounded-xl w-full">
      <h2 className="text-gray-500">{title}</h2>
      <p className="text-2xl font-bold">₹{amount / 100}</p>
    </div>
  );
}