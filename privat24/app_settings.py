# -*- coding: utf-8 -*-
import os
from django.conf import settings

PRIVAT24_TRANSACTION_MODEL = getattr(settings, 'PRIVAT24_TRANSACTION_MODEL', 'privat24.privat24transaction')

default_options = {
        'merchant': '100000',
        'password': '3F9du1eVH3PJhgZ1cXPVphJ861DM0S1',
        'test_mode': True,
        'return_url':'http://example.com/payments/', #страница, принимающая клиента после оплаты
        'server_url':'http://example.com/p24/notify-handler/', #страница, принимающая ответ API о результате платежа
}

if hasattr(settings, 'PRIVAT24_OPTIONS'):
    setted_options =  getattr(settings, 'PRIVAT24_OPTIONS')
    if setted_options:
        PRIVAT24_OPTIONS = setted_options
    else:
        PRIVAT24_OPTIONS = default_options
else:
    PRIVAT24_OPTIONS = default_options
