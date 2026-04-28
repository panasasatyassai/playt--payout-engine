const BASE_URL = import.meta.env.VITE_API_URL;

// 👉 Get Dashboard
export const getDashboard = async (merchantId) => {
  const res = await fetch(`${BASE_URL}/dashboard/${merchantId}/`);
  const data = await res.json();

  // ❌ if API failed
  if (!data.success) {
    throw new Error(data.error || "Failed to fetch dashboard");
  }

  // ✅ return only actual data
  return data.data;
};

// 👉 Create Merchant
export const createMerchant = async (data) => {
  const res = await fetch(`${BASE_URL}/merchant/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const dataJson = await res.json();

  if (!res.ok) {
    throw new Error(dataJson.error || "Failed to create merchant");
  }

  if (dataJson.error) {
    throw new Error(dataJson.error);
  }

  return dataJson;
};

// 👉 Get all merchants
export const getMerchants = async () => {
  const res = await fetch(`${BASE_URL}/merchants/`);
  return res.json();
};

// 👉 Simulate Client Payment
export const simulatePayment = async (merchantId, amount) => {
  const res = await fetch(`${BASE_URL}/simulate-payment/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      merchant_id: merchantId,
      amount_paise: amount,
    }),
  });

  return res.json();
};

export const getClientPayments = async (merchantId) => {
  const res = await fetch(`${BASE_URL}/client-payments/${merchantId}/`);
  return res.json();
};

// 👉 Create Payout
// export const createPayout = async (merchantId, amount) => {
//   const res = await fetch(`${BASE_URL}/payouts/`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "Idempotency-Key": crypto.randomUUID(), // 🔥 IMPORTANT
//     },
//     body: JSON.stringify({
//       merchant_id: merchantId,
//       amount_paise: amount,
//     }),
//   });

//   return res.json();
// };

export const createPayout = async (merchantId, amount, key) => {
  const res = await fetch(`${BASE_URL}/v1/payouts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Idempotency-Key": key,
    },
    body: JSON.stringify({
      merchant_id: merchantId,
      amount_paise: amount,
      bank_account_id: "TEST_BANK_123", // ✅ ADD THIS
    }),
  });

  const data = await res.json();

  if (!res.ok || data.success === false) {
    throw new Error(data.error || data.message || "Payout failed");
  }

  return data;
};

// export const getDashboard = (merchantId) => {
//   return API.get(`/dashboard/${merchantId}/`);
// };