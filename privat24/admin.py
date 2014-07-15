from django.contrib import admin

from . import get_privat24_transaction_model
TransactionModel = get_privat24_transaction_model()

admin.site.register(TransactionModel)

