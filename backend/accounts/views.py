from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from ledger.models import Ledger
from .models import Merchant
from accounts.tasks import process_payouts
from payouts.models import Payout

def dashboard(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)

        # ✅ total credits
        credits = Ledger.objects.filter(
            merchant=merchant,
            transaction_type="credit"
        ).aggregate(total=Sum("amount"))["total"] or 0

        # ✅ total debits
        debits = Ledger.objects.filter(
            merchant=merchant,
            transaction_type="debit"
        ).aggregate(total=Sum("amount"))["total"] or 0

        # ✅ available balance
        available_balance = credits - debits

        # ✅ HELD BALANCE (IMPORTANT)
        held_balance = Payout.objects.filter(
            merchant=merchant,
            status__in=["pending", "processing"]
        ).aggregate(total=Sum("amount_paise"))["total"] or 0

        return JsonResponse({
            "available_balance": available_balance,
            "held_balance": held_balance
        })

    except Merchant.DoesNotExist:
        return JsonResponse({"error": "Merchant not found"}, status=404)

def client_payments_summary(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return JsonResponse({"error": "Merchant not found"}, status=404)

    # ✅ Only client payments
    total_client_payments = Ledger.objects.filter(
        merchant=merchant,
        transaction_type="credit",
        description="Client payment"
    ).aggregate(total=Sum("amount"))["total"] or 0

    return JsonResponse({
        "merchant_id": merchant.id,
        "client_payments_total": total_client_payments
    })

@csrf_exempt
def simulate_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        merchant_id = data.get("merchant_id")
        amount = data.get("amount_paise")

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return JsonResponse({"error": "Merchant not found"}, status=404)

        # ✅ Create CREDIT entry (Client Payment)
        Ledger.objects.create(
            merchant=merchant,
            amount=amount,
            transaction_type="credit",
            description="Client payment"
        )

        return JsonResponse({"message": "Payment simulated successfully"})

# ===============================
# ▶ Run payout processor
# ===============================
def run_payout_processor(request):
    process_payouts()
    return JsonResponse({"message": "Processor executed"})


# ===============================
# ▶ Merchant Dashboard
# ===============================
# def merchant_dashboard(request, merchant_id):
#     try:
#         merchant = Merchant.objects.get(id=merchant_id)
#     except Merchant.DoesNotExist:
#         return JsonResponse({"error": "Merchant not found"}, status=404)

#     # ✅ DB aggregation (IMPORTANT)
#     total_credit = Ledger.objects.filter(
#         merchant=merchant,
#         transaction_type='credit'
#     ).aggregate(total=Sum('amount'))['total'] or 0

#     total_debit = Ledger.objects.filter(
#         merchant=merchant,
#         transaction_type='debit'
#     ).aggregate(total=Sum('amount'))['total'] or 0

#     balance = total_credit - total_debit

#     # ✅ Transactions
#     transactions = Ledger.objects.filter(merchant=merchant)

#     txn_list = list(
#         transactions.values('amount', 'transaction_type', 'created_at')
#     )

#     return JsonResponse({
#         "merchant": {
#             "id": merchant.id,
#             "name": merchant.name,
#             "email": merchant.email
#         },
#         "balance_paise": balance,
#         "total_credit": total_credit,
#         "total_debit": total_debit,
#         "transactions": txn_list
#     })

# def merchant_dashboard(request, merchant_id):
#     try:
#         merchant = Merchant.objects.get(id=merchant_id)
#     except Merchant.DoesNotExist:
#         return JsonResponse({"error": "Merchant not found"}, status=404)

#     # ✅ Ledger summary (DB level calculation)
#     total_credit = Ledger.objects.filter(
#         merchant=merchant,
#         transaction_type='credit'
#     ).aggregate(total=Sum('amount'))['total'] or 0

#     total_debit = Ledger.objects.filter(
#         merchant=merchant,
#         transaction_type='debit'
#     ).aggregate(total=Sum('amount'))['total'] or 0

#     balance = total_credit - total_debit

#     # ✅ Recent ledger entries
#     ledger_entries = Ledger.objects.filter(
#         merchant=merchant
#     ).order_by('-created_at')[:10]

#     ledger_data = list(
#         ledger_entries.values('amount', 'transaction_type', 'description', 'created_at')
#     )

#     # ✅ Payout history
#     payouts = Payout.objects.filter(
#         merchant=merchant
#     ).order_by('-created_at')[:10]

#     payout_data = list(
#         payouts.values('amount_paise', 'status', 'attempts', 'created_at')
#     )

#     return JsonResponse({
#         "merchant": {
#             "id": merchant.id,
#             "name": merchant.name,
#             "email": merchant.email
#         },

#         # ✅ Balance split (IMPORTANT)
#         # "available_balance": merchant.available_balance,
#         # "held_balance": merchant.held_balance,

#         # ✅ Derived balance (ledger)
#         "ledger_balance": balance,
#         "total_credit": total_credit,
#         "total_debit": total_debit,

#         "recent_transactions": ledger_data,
#         "payouts": payout_data
#     })

def merchant_dashboard(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return JsonResponse({"error": "Merchant not found"}, status=404)

    # ✅ CREDIT
    # credits = Ledger.objects.filter(
    #     merchant=merchant,
    #     transaction_type="credit" , 
    #     description="Client payment" 
    # ).aggregate(total=Sum("amount"))["total"] or 0

    # # ✅ DEBIT
    # debits = Ledger.objects.filter(
    #     merchant=merchant,
    #     transaction_type="debit"
    # ).aggregate(total=Sum("amount"))["total"] or 0

    # ✅ BALANCE
    # balance = credits - debits

    # ==========================
# 🔥 AVAILABLE BALANCE (ALL credits including refunds)
# ==========================
    all_credits = Ledger.objects.filter(
        merchant=merchant,
        transaction_type="credit"
    ).aggregate(total=Sum("amount"))["total"] or 0

    all_debits = Ledger.objects.filter(
        merchant=merchant,
        transaction_type="debit"
    ).aggregate(total=Sum("amount"))["total"] or 0


        # 🔥 HELD BALANCE (THIS WAS MISSING)
    held_balance = Payout.objects.filter(
            merchant=merchant,
            status__in=["pending", "processing"]
        ).aggregate(total=Sum("amount_paise"))["total"] or 0

    # ==========================
# 🔥 TOTAL CREDIT (ONLY CLIENT MONEY)
# ==========================
    # client_credits = Ledger.objects.filter(
    #     merchant=merchant,
    #     transaction_type="credit",
    #     description="Client payment"
    # ).aggregate(total=Sum("amount"))["total"] or 0
    # 🔥 ONLY CLIENT PAYMENTS
    # 🔥 TOTAL CREDIT (ALL credits including refunds)
    total_credit = Ledger.objects.filter(
        merchant=merchant,
        transaction_type="credit"
    ).aggregate(total=Sum("amount"))["total"] or 0


        # 🔥 HELD BALANCE (THIS WAS MISSING)
         

        # 🔥 ONLY CLIENT PAYMENTS
    client_payments = Ledger.objects.filter(
        merchant=merchant,
        transaction_type="credit",
        description="Client payment"
    ).aggregate(total=Sum("amount"))["total"] or 0

    balance = all_credits - all_debits

    # ✅ TRANSACTIONS
    transactions = list(
        Ledger.objects.filter(merchant=merchant)
        .order_by("-created_at")
        .values("amount", "transaction_type", "description", "created_at")
    )

    # ✅ PAYOUTS
    payouts = list(
        Payout.objects.filter(merchant=merchant)
        .order_by("-created_at")
        .values("amount_paise", "status", "attempts", "created_at")
    )

    return JsonResponse({
        "success": True,
        "data": {
            "merchant": {
                "id": merchant.id,
                "name": merchant.name,
                "email": merchant.email
            },
            "ledger_balance": balance,
            "total_credit": total_credit,
            "total_debit": all_debits,
            "client_payments": client_payments,
            "held_balance": held_balance,
            "recent_transactions": transactions,
            "payouts": payouts
        }
    })
# ===============================
# ▶ Create Merchant
# ===============================
@csrf_exempt
def create_merchant(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return JsonResponse({"error": "Name and email required"}, status=400)

        merchant = Merchant.objects.create(
            name=name,
            email=email
        )

        return JsonResponse({
            "message": "Merchant created successfully",
            "merchant": {
                "id": merchant.id,
                "name": merchant.name,
                "email": merchant.email
            }
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ===============================
# ▶ Create Transaction (Credit Only)
# ===============================
@csrf_exempt
def create_transaction(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)

        merchant_id = data.get("merchant_id")
        amount = data.get("amount_paise")
        txn_type = data.get("transaction_type")

        merchant = Merchant.objects.get(id=merchant_id)

        # ✅ Validate
        if txn_type not in ['credit', 'debit']:
            return JsonResponse({"error": "Invalid transaction type"}, status=400)

        # ✅ Calculate balance (DB-level)
        total_credit = Ledger.objects.filter(
            merchant=merchant,
            transaction_type='credit'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_debit = Ledger.objects.filter(
            merchant=merchant,
            transaction_type='debit'
        ).aggregate(total=Sum('amount'))['total'] or 0

        balance = total_credit - total_debit

        # ❌ Prevent overdraft
        if txn_type == 'debit' and amount > balance:
            return JsonResponse({"error": "Insufficient balance"}, status=400)

        # ✅ Create Ledger entry
        txn = Ledger.objects.create(
            merchant=merchant,
            amount=amount,
            transaction_type=txn_type,
            description="Manual transaction"
        )

        return JsonResponse({
            "message": "Transaction created",
            "transaction": {
                "merchant": merchant.name,
                "amount": txn.amount,
                "transaction_type": txn.transaction_type
            }
        })

    except Merchant.DoesNotExist:
        return JsonResponse({"error": "Merchant not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ===============================
# ▶ Get Balance
# ===============================
def get_balance(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return JsonResponse({"error": "Merchant not found"}, status=404)

    total_credit = Ledger.objects.filter(
        merchant=merchant,
        transaction_type='credit'
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_debit = Ledger.objects.filter(
        merchant=merchant,
        transaction_type='debit'
    ).aggregate(total=Sum('amount'))['total'] or 0

    balance = total_credit - total_debit

    transactions = Ledger.objects.filter(merchant=merchant)

    txn_list = list(
        transactions.values('transaction_type', 'amount', 'created_at')
    )

    return JsonResponse({
        "merchant": merchant.name,
        "balance_paise": balance,
        "transactions": txn_list
    })

# 👉 Get All Merchants
def get_merchants(request):
    merchants = Merchant.objects.all().values("id", "name", "email")
    return JsonResponse(list(merchants), safe=False)