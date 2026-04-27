import threading
import time
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # def ready(self):
    #     from accounts.tasks import process_payouts

    #     def start_worker():
    #         while True:
    #             process_payouts()
    #             time.sleep(10)  # run every 10 seconds

    #     # start background thread
    #     threading.Thread(target=start_worker, daemon=True).start()