# 💸 Playto Payout Engine

🔗 **GitHub Repository:**
https://github.com/panasasatyassai/playt--payout-engine

🌐 **Live Demo:**
Frontend: https://your-frontend-url.vercel.app
Backend API: https://your-backend-url.onrender.com

---

## 🚀 Project Overview

Playto Payout Engine is a **full-stack financial simulation system** that mimics real-world merchant payments, balances, and payout processing.

It demonstrates:

* Payment lifecycle
* Payout processing
* Idempotency handling
* Background job execution using Celery

---

## ✨ Features

### 🧑‍💼 Merchant Management

* Create merchants
* View all merchants
* Navigate to dashboard

### 💰 Payments

* Simulate incoming client payments
* Automatically update merchant balance

### 📤 Payout Engine

* Create payouts with idempotency
* Status handling:

  * ✅ Completed (70%)
  * ❌ Failed (20%)
  * 🔁 Retry (10%)

### ⚙️ Background Processing

* Celery + Redis
* Runs every 10 seconds
* Processes pending payouts automatically

### 📊 Dashboard

* Merchant balance
* Transactions (credit/debit)
* Payout history

---

## 🏗️ Tech Stack

### Backend

* Django
* Django REST Framework
* PostgreSQL
* Celery
* Redis

### Frontend

* React (Vite)
* Tailwind CSS
* React Router
* React Icons

---

## 📂 Project Structure

```bash
project/
│
├── backend/
│   ├── accounts/
│   ├── payouts/
│   ├── ledger/
│   └── core/
│
├── frontend/
│   └── frontend/
│       ├── src/
│       ├── components/
│       └── pages/
│
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 🔹 Clone Repo

```bash
git clone https://github.com/panasasatyassai/playt--payout-engine.git
cd project
```

---

### 🔹 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=playto_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
```

Run:

```bash
python manage.py migrate
python manage.py runserver
```

---

### 🔹 Celery Setup

```bash
celery -A core worker -l info
celery -A core beat -l info
```

---

### 🔹 Frontend Setup

```bash
cd frontend/frontend
npm install
npm run dev
```

Create `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

---

## 🌐 API Documentation

### 🧑‍💼 Merchant APIs

#### Create Merchant

```
POST /api/merchant/create/
```

#### Get All Merchants

```
GET /api/merchants/
```

#### Merchant Dashboard

```
GET /api/dashboard/<merchant_id>/
```

---

### 💰 Transaction APIs

#### Create Transaction

```
POST /api/transaction/create/
```

#### Get Transactions

```
GET /api/transactions/<merchant_id>/
```

#### Get Balance

```
GET /api/balance/<merchant_id>/
```

---

### 💳 Payment APIs

#### Simulate Payment

```
POST /api/simulate-payment/
```

#### Client Payment Summary

```
GET /api/client-payments/<merchant_id>/
```

---

### 📤 Payout APIs

#### Create Payout (Idempotent)

```
POST /api/v1/payouts
```

Headers:

```
Idempotency-Key: unique-key
```

Body:

```json
{
  "merchant_id": 1,
  "amount_paise": 5000,
  "bank_account_id": "TEST_BANK_123"
}
```

---

#### Run Processor (Manual)

```
GET /api/run-processor/
```

---

## 🔄 Frontend API Usage

```js
const BASE_URL = import.meta.env.VITE_API_URL;
```

Example:

```js
GET ${BASE_URL}/dashboard/:merchantId/
```

---

## 🚀 Deployment

### Backend (Render)

* Add environment variables:

  * SECRET_KEY
  * DATABASE
  * REDIS URL

### Frontend (Vercel)

```env
VITE_API_URL=https://your-backend-url.onrender.com/api
```

---

## 🔐 Security

* ❌ Do NOT push `.env` files
* ❌ Do NOT expose SECRET_KEY
* ✅ Use environment variables in deployment

---

## 🧠 System Design (Simplified Flow)

```
Client Payment → Ledger Entry → Balance Update
                          ↓
                    Create Payout
                          ↓
                  Celery Worker (Async)
                          ↓
                Success / Failure / Retry
                          ↓
                     Dashboard Update
```

---
 
## 👨‍💻 Author

**Panasa Satya Sai**

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🚀 Build more features

---
