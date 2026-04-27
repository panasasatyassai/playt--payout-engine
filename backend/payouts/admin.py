from django.contrib import admin
from .models import Payout

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'merchant',
        'amount_paise',
        'status',
        'attempts',          # ✅ THIS YOU WANT
        'last_attempt_at',   # optional
        'created_at'
    )