from django.db import models
from django.core.exceptions import ValidationError   # 🔥 IMPORTANT (you missed this)
from accounts.models import Merchant


class Payout(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="payouts",
        db_index=True
    )

    amount_paise = models.BigIntegerField()  # ✅ always in paise

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    # ✅ Retry tracking
    attempts = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(null=True, blank=True)

    # ✅ Idempotency
    idempotency_key = models.CharField(max_length=255, unique=True)

    # ✅ Bank account
    bank_account_id = models.CharField(max_length=100, null=True, blank=True)

    # ✅ Store response (important for idempotency)
    response_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "idempotency_key"],
                name="unique_idempotency_per_merchant"
            )
        ]

    # ==========================
    # 🔥 STATE MACHINE LOGIC
    # ==========================
    def can_transition(self, new_status):
        allowed_transitions = {
            "pending": ["processing"],
            "processing": ["completed", "failed"],
            "completed": [],
            "failed": []
        }
        return new_status in allowed_transitions.get(self.status, [])

    def update_status(self, new_status):
        if not self.can_transition(new_status):
            raise ValidationError(
                f"Invalid transition: {self.status} → {new_status}"
            )

        self.status = new_status
        self.save()

    def __str__(self):
        return f"Payout {self.id} | {self.merchant.name} | ₹{self.amount_paise/100} | {self.status}"