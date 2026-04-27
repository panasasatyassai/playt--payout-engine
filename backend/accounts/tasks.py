import random
from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from payouts.models import Payout
from ledger.models import Ledger

from core.celery import app
from celery import shared_task


def process_payouts():
    now = timezone.now()

    payouts = Payout.objects.filter(
        status__in=['pending', 'processing']
    )

    for payout in payouts:
        with transaction.atomic():

            # 🔒 LOCK payout row (IMPORTANT)
            payout = Payout.objects.select_for_update().get(id=payout.id)

            # ✅ Skip final states
            if payout.status in ['completed', 'failed']:
                continue

            # ==========================
            # 🔁 Retry delay
            # ==========================
            if payout.status == 'processing':
                if payout.last_attempt_at:
                    diff = now - payout.last_attempt_at
                    if diff < timedelta(seconds=30):
                        continue

            # ==========================
            # ❌ Max attempts → FAIL (ONLY ONCE)
            # ==========================
            if payout.attempts >= 3 and payout.status != 'failed':
                payout.status = 'failed'

                Ledger.objects.create(
                    merchant=payout.merchant,
                    amount=payout.amount_paise,
                    transaction_type='credit',
                    description='Refund after max retry failure'
                )

                payout.save()
                continue

            # ==========================
            # 🚀 Move to processing
            # ==========================
            if payout.status == 'pending':
                payout.status = 'processing'

            payout.attempts += 1
            payout.last_attempt_at = now
            payout.save()

            # ==========================
            # 🎲 Simulate bank response
            # ==========================
            rand = random.randint(1, 100)

            # ✅ SUCCESS
            if rand <= 70:
                payout.status = 'completed'

            # ❌ FAILURE
            elif rand <= 90:
                if payout.status != 'failed':  # prevent duplicate refund
                    payout.status = 'failed'

                    Ledger.objects.create(
                        merchant=payout.merchant,
                        amount=payout.amount_paise,
                        transaction_type='credit',
                        description='Refund after failed payout'
                    )

            # ⏳ STUCK
            else:
                payout.save()
                continue

            payout.save()

@shared_task
def process_payouts_task():
    process_payouts()
    return "Task completed"