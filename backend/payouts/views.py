import uuid
import json
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from payouts.models import Payout
from accounts.models import Merchant
from ledger.models import Ledger
from payouts.tasks import process_payout_task


@csrf_exempt
def create_payout(request):

    # ==========================
    # ✅ Method check
    # ==========================
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "POST required"
        }, status=400)

    # ==========================
    # ✅ Idempotency key
    # ==========================
    idempotency_key = request.headers.get("Idempotency-Key")

    if not idempotency_key:
        return JsonResponse({
            "success": False,
            "error": "Idempotency-Key required"
        }, status=400)

    # ✅ Validate UUID
    try:
        uuid.UUID(idempotency_key)
    except:
        return JsonResponse({
            "success": False,
            "error": "Invalid Idempotency-Key"
        }, status=400)

    # ==========================
    # ✅ Parse JSON
    # ==========================
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON"
        }, status=400)

    merchant_id = data.get("merchant_id")
    amount = data.get("amount_paise")
    bank_account_id = data.get("bank_account_id")

    # ==========================
    # ✅ Validate input
    # ==========================
    if not merchant_id or not amount or not bank_account_id:
        return JsonResponse({
            "success": False,
            "error": "Invalid data"
        }, status=400)

    # ==========================
    # ✅ Bank Account Validation
    # ==========================
    if not bank_account_id or len(bank_account_id.strip()) == 0:
        return JsonResponse({
            "success": False,
            "error": "Bank account ID required"
        }, status=400)

    try:
        amount = int(amount)
    except:
        return JsonResponse({
            "success": False,
            "error": "Invalid amount"
        }, status=400)

    if amount <= 0:
        return JsonResponse({
            "success": False,
            "error": "Invalid amount"
        }, status=400)

    try:
        with transaction.atomic():

            # 🔒 Lock merchant (prevents race condition)
            merchant = Merchant.objects.select_for_update().get(id=merchant_id)

            # ==========================
            # ✅ STRICT IDEMPOTENCY
            # ==========================
            existing = Payout.objects.filter(
                merchant=merchant,
                idempotency_key=idempotency_key,
                created_at__gte=timezone.now() - timedelta(hours=24)
            ).first()

            if existing:
                if existing.response_data:
                    return JsonResponse(existing.response_data)
                else:
                    return JsonResponse({
                        "success": True,
                        "data": {
                            "payout_id": existing.id,
                            "status": existing.status
                        }
                    })

            # ==========================
            # ✅ Balance calculation
            # ==========================
            credits = Ledger.objects.filter(
                merchant=merchant,
                transaction_type='credit'
            ).aggregate(total=Sum('amount'))['total'] or 0

            debits = Ledger.objects.filter(
                merchant=merchant,
                transaction_type='debit'
            ).aggregate(total=Sum('amount'))['total'] or 0

            balance = credits - debits

            if amount > balance:
                return JsonResponse({
                    "success": False,
                    "error": "Insufficient balance"
                }, status=400)

            # ==========================
            # ✅ HOLD money (debit)
            # ==========================
            Ledger.objects.create(
                merchant=merchant,
                amount=amount,
                transaction_type='debit',
                description="Payout requested"
            )

            # ==========================
            # ✅ Create payout
            # ==========================
            payout = Payout.objects.create(
                merchant=merchant,
                amount_paise=amount,
                idempotency_key=idempotency_key,
                bank_account_id=bank_account_id,
                status='pending'
            )

            response = {
                "success": True,
                "data": {
                    "payout_id": payout.id,
                    "status": payout.status
                }
            }

            # ==========================
            # 🔥 Trigger Celery
            # ==========================
            process_payout_task.delay(payout.id)

            # ==========================
            # ✅ Store response (idempotency)
            # ==========================
            payout.response_data = response
            payout.save()

            return JsonResponse(response)

    except Merchant.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Merchant not found"
        }, status=404)