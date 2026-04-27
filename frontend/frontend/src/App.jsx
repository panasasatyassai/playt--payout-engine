import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Dashboard from "./pages/Dashboard";
import CreateMerchant from "./pages/CreateMerchant";

function App() {
  return (
    <BrowserRouter>
      <Toaster 
        position="top-center"
        reverseOrder={false}
        gutter={8}
        toastOptions={{
          duration: 3000,
          style: {
            background: "#fff",
            color: "#000",
          },
          success: {
            style: {
              background: "#10b981",
              color: "#fff",
            },
          },
          error: {
            style: {
              background: "#ef4444",
              color: "#fff",
            },
          },
        }}
      />
      <Routes>
        <Route path="/" element={<CreateMerchant />} />
        <Route path="/dashboard/:id" element={<Dashboard />} /> {/* 🔥 */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;