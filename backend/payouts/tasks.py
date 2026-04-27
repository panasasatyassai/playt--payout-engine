import random
from datetime import timedelta
import logging

from celery import shared_task
from django.utils import timezone
from django.db import transaction

from payouts.models import Payout
from ledger.models import Ledger

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_payout_task(self, payout_id):
    try:
        logger.info(f"Processing payout {payout_id}")
        payout = Payout.objects.get(id=payout_id)

        # ==========================
        # ✅ Skip if already final
        # ==========================
        if payout.status in ["completed", "failed"]:
            return

        now = timezone.now()

        # ==========================
        # ✅ Retry delay (30 sec rule)
        # ==========================
        if payout.status == "processing":
            if payout.last_attempt_at:
                diff = now - payout.last_attempt_at
                if diff < timedelta(seconds=30):
                    return

        with transaction.atomic():

            payout.refresh_from_db()

            # ==========================
            # ✅ Max retry reached
            # ==========================
            if payout.attempts >= 3:
                payout.update_status("failed")
                logger.error(f"Payout {payout.id} failed after max retries")

                # 🔥 refund money
                Ledger.objects.create(
                    merchant=payout.merchant,
                    amount=payout.amount_paise,
                    transaction_type="credit",
                    description="Refund after max retry failure"
                )

                return

            # ==========================
            # ✅ Move to processing
            # ==========================
            payout.update_status("processing")
            payout.attempts += 1
            payout.last_attempt_at = now
            payout.save()
            logger.info(f"Attempt {payout.attempts} for payout {payout.id}")

            # ==========================
            # 🎯 70 / 20 / 10 logic
            # ==========================
            rand = random.randint(1, 100)
            logger.info(f"Payout {payout.id} random outcome: {rand}")
            # ✅ 70% SUCCESS
            if rand <= 70:
                payout.update_status("completed")
                logger.info(f"Payout {payout.id} completed")

            # ❌ 20% FAILURE
            elif rand <= 90:
                payout.update_status("failed")
                logger.error(f"Payout {payout.id} failed")

                # 🔥 refund
                Ledger.objects.create(
                    merchant=payout.merchant,
                    amount=payout.amount_paise,
                    transaction_type="credit",
                    description="Refund after failed payout"
                )

            # ⏳ 10% STUCK (no change)
            else:
                return

    except Exception as e:
        # ==========================
        # 🔁 EXPONENTIAL BACKOFF
        # ==========================
        retry_delay = 2 ** self.request.retries

        logger.warning(f"Retrying payout {payout_id}, attempt {self.request.retries + 1}, delay {retry_delay}s")

        raise self.retry(exc=e, countdown=retry_delay)