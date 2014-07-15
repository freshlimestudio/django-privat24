# coding: UTF-8
from . import app_settings
from privat24 import models

def get_options():
    options = {
        'merchant_id': '',  # Must be set in settings.py
        'password': '',     # Must be set in settings.py
        'return_url': '',   # Must be set in settings.py
        'server_url': '',   # Must be set in settings.py
        'ccy': models.P24_CCY_UAH,
        'pay_way': 'privat24',
        'test_mode': True,
    }
    settings_opts = {}
    try:
        settings_opts = app_settings.PRIVAT24_OPTIONS
    except AttributeError:
        pass
    options.update(settings_opts)
    return options

