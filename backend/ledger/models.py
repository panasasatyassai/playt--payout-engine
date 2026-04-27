from django.db import models
from accounts.models import Merchant


class Ledger(models.Model):

    class TransactionType(models.TextChoices):
        CREDIT = "credit", "Credit"
        DEBIT = "debit", "Debit"

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="ledgers",
        db_index=True
    )

    amount = models.BigIntegerField()  # ✅ always in paise

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        db_index=True
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]  # latest first
        indexes = [
            models.Index(fields=["merchant", "transaction_type"]),
        ]

    def __str__(self):
        return f"{self.merchant.name} | {self.transaction_type} | ₹{self.amount/100}"