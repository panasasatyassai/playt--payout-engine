import { useState, useEffect } from "react";
import toast from "react-hot-toast";
import { createMerchant, getMerchants } from "../services/api";
import { useNavigate } from "react-router-dom";
import { FaUserPlus, FaEnvelope, FaUserCircle } from "react-icons/fa";

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
      } else if (
        message.toLowerCase().includes("already exists") ||
        message.toLowerCase().includes("unique constraint")
      ) {
        toast.error("Record already exists");
      } else {
        toast.error(message);
      }

      setEmail("");
      setName("");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* HEADER */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">
          Merchant Management
        </h1>
        <p className="text-gray-500">Create and manage merchants</p>
      </div>

      {/* GRID */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* CREATE FORM */}
        <div className="bg-white p-6 rounded-xl shadow border">
          <div className="flex items-center gap-2 mb-4">
            <FaUserPlus className="text-blue-500 text-xl" />
            <h2 className="text-xl font-semibold">Create Merchant</h2>
          </div>

          {/* NAME */}
          <div className="flex items-center border rounded px-3 py-2 mb-3 focus-within:ring-2 focus-within:ring-blue-400">
            <FaUserCircle className="text-gray-400 mr-2" />
            <input
              type="text"
              placeholder="Enter name"
              className="w-full outline-none"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          {/* EMAIL */}
          <div className="flex items-center border rounded px-3 py-2 mb-4 focus-within:ring-2 focus-within:ring-blue-400">
            <FaEnvelope className="text-gray-400 mr-2" />
            <input
              type="email"
              placeholder="Enter email"
              className="w-full outline-none"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          {/* BUTTON */}
          <button
            onClick={handleCreate}
            className="w-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white py-2 rounded-lg hover:opacity-90 transition"
          >
            Create Merchant
          </button>
        </div>

        {/* MERCHANT LIST */}
        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow border">
            <h2 className="text-xl font-semibold mb-4">Merchants</h2>

            {merchants.length === 0 ? (
              <p className="text-gray-500 text-center py-10">
                No merchants yet
              </p>
            ) : (
              <div className="space-y-3 max-h-[500px] overflow-y-auto">
                {merchants.map((m) => (
                  <div
                    key={m.id}
                    onClick={() => navigate(`/dashboard/${m.id}`)}
                    className="flex items-center justify-between p-4 border rounded-lg hover:shadow-md hover:bg-gray-50 cursor-pointer transition"
                  >
                    <div className="flex items-center gap-3">
                      <FaUserCircle className="text-3xl text-blue-500" />
                      <div>
                        <p className="font-semibold text-gray-800">{m.name}</p>
                        <p className="text-sm text-gray-500">{m.email}</p>
                      </div>
                    </div>

                    <span className="text-sm text-blue-500 font-medium">
                      View →
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
