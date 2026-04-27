from django.contrib import admin
from django.urls import path
from accounts.views import get_balance
from ledger.views import   get_transactions
from accounts.views import create_transaction
# from accounts.views import create_merchant
# from accounts.views import merchant_dashboard
from accounts.views import run_payout_processor
from payouts.views import create_payout
from accounts.views import simulate_payment
from accounts.views import client_payments_summary
from accounts.views import dashboard

from accounts.views import (
    create_merchant,
    get_merchants,
    merchant_dashboard
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Balance API
    path('api/balance/<int:merchant_id>/', get_balance),

        # NEW Transactions API
    path('api/transactions/<int:merchant_id>/', get_transactions),

    # create transation without admin
    path('api/transaction/create/', create_transaction),

    # create merchant without admin
    path('api/merchant/create/', create_merchant),
    path('api/merchants/', get_merchants),


    #get mrchant details
    path('api/dashboard/<int:merchant_id>/', merchant_dashboard),

    #payout api 
    path('api/v1/payouts', create_payout), 

    path('api/run-processor/', run_payout_processor),

    path('api/simulate-payment/', simulate_payment),

     path("dashboard/<int:merchant_id>/", dashboard),

    path("api/client-payments/<int:merchant_id>/", client_payments_summary),
]