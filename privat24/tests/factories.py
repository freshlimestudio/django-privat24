# -*- coding: utf-8 -*-
import factory
from django.utils import timezone
from decimal import Decimal

from .. import get_privat24_transaction_model
TransactionModel = get_privat24_transaction_model()

class Privat24TransactionFactory(factory.Factory):
    FACTORY_FOR = TransactionModel
    amt = Decimal("123.45")                         # сумма, 1.0&
    ccy = 'UAH'                                     # валюта, UAH|USD|EUR&
    details = 'Test payment'                        # назначение&
    pay_way = 'privat24'                            # privat24&
    order = str(factory.Sequence(lambda n: n))      # order_id, 1&
    merchant = str(factory.Sequence(lambda n: n))   # merchant id, 1&
    state = 'test'                                  # ок|fail|test&
    date = str(timezone.now().date())               # 010113232010 (фомат ddMMyyHHmmss)
    signature = 'signature'                         # сигнатура
