export default function SkeletonCard() {
  return (
    <div className="bg-white p-6 rounded-xl shadow animate-pulse">
      <div className="h-4 bg-gray-300 rounded w-1/2 mb-3"></div>
      <div className="h-6 bg-gray-400 rounded w-1/3"></div>
    </div>
  );
}
