import { useState, useEffect } from "react";
import toast from "react-hot-toast";
import { createMerchant, getMerchants } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function CreateMerchant() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [merchants, setMerchants] = useState([]);

  const navigate = useNavigate();

  // 🔥 Load merchants
  const loadMerchants = async () => {
    const data = await getMerchants();
    setMerchants(data);
  };

  useEffect(() => {
    loadMerchants();
  }, []);

  // 🔥 Create merchant
  const handleCreate = async () => {
    if (!name || !email) {
      return toast.error("Enter all fields");
    }

    try {
      await createMerchant({ name, email });

      setName("");
      setEmail("");

      loadMerchants(); // refresh list
      toast.success("Merchant created successfully!");
    } catch (err) {
      console.error("Create merchant error:", err);
      const message = err?.message || "Failed to create merchant";
      
      // Check for both name and email
      const hasNameError = message.toLowerCase().includes("name");
      const hasEmailError = message.toLowerCase().includes("email");
      
      if (hasNameError && hasEmailError) {
        toast.error("Name and email already exists");
      } else if (hasEmailError) {
        toast.error("Email already exists");
      } else if (hasNameError) {
        toast.error("Name already exists");
      } else if (message.toLowerCase().includes("already exists") || message.toLowerCase().includes("unique constraint")) {
        toast.error("Record already exists");
      } else {
        toast.error(message);
      }
      
      setEmail("");
      setName("");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Create Merchant</h1>

      {/* FORM */}
      <div className="bg-white p-4 shadow rounded w-80 mb-6">
        <input
          className="border p-2 w-full mb-2"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="border p-2 w-full mb-2"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <button
          onClick={handleCreate}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Create
        </button>
      </div>

      {/* MERCHANT LIST */}
      <h2 className="text-xl font-semibold mb-2">Merchants</h2>

      {merchants.length === 0 ? (
        <p className="text-gray-500">No merchants yet</p>
      ) : (
        merchants.map((m) => (
          <div
            key={m.id}
            onClick={() => navigate(`/dashboard/${m.id}`)}
            className="bg-white p-3 mb-2 shadow rounded cursor-pointer hover:bg-gray-100"
          >
            <p className="font-semibold">{m.name}</p>
            <p className="text-sm text-gray-500">{m.email}</p>
          </div>
        ))
      )}
    </div>
  );
}