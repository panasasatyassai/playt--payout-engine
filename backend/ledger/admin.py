from django.contrib import admin
from .models import Ledger


@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ("id", "merchant", "transaction_type", "amount", "created_at")