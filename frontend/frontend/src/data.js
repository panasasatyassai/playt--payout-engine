export const dashboardData = {
  available_balance: 70000,
  held_balance: 900,
  ledger_balance: 69100,

  transactions: [
    { id: 1, type: "credit", amount: 80000 },
    { id: 2, type: "debit", amount: 800 },
  ],

  payouts: [
    { id: 1, amount: 900, status: "pending" },
    { id: 2, amount: 900, status: "completed" },
    { id: 3, amount: 799, status: "failed" },
  ]
};