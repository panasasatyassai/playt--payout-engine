from django.http import JsonResponse
from ledger.models import Ledger   # ✅ FIXED
from accounts.models import Merchant


def get_transactions(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return JsonResponse({"error": "Merchant not found"}, status=404)

    # ✅ fetch ledger entries
    transactions = Ledger.objects.filter(merchant=merchant).order_by('-created_at')

    data = []

    for txn in transactions:
        data.append({
            "amount": txn.amount,   # ✅ FIXED
            "transaction_type": txn.transaction_type,
            "description": txn.description,
            "created_at": txn.created_at
        })

    return JsonResponse({
        "merchant": merchant.name,
        "transactions": data
    })