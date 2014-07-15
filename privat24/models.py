# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

P24_CCY_UAH = 'UAH'
P24_CCY_USD = 'USD'
P24_CCY_EUR = 'EUR'
P24_CCY_CHOICES = (
    (P24_CCY_UAH, _('UAH')),
    (P24_CCY_USD, _('USD')),
    (P24_CCY_EUR, _('EUR')),
)

P24_STATE_OK = 'ok'
P24_STATE_FAIL = 'fail'
P24_STATE_TEST = 'test'
P24_STATE_CHOICES = (
    (P24_STATE_OK, _('ok')),
    (P24_STATE_FAIL, _('fail')),
    (P24_STATE_TEST, _('test')),
)

class AbstractPrivat24Transaction(models.Model):
    """
    An abstract base class implementing a fully featured Privat24Transaction model

    amt, ccy, details, pay_way, order, merchant, state, date and encoding are required. Other fields are optional.
    """

    amt = models.DecimalField(_('amount'), max_digits=16, decimal_places=2, default=0)      # сумма, 1.0&
    ccy = models.CharField(_('ccy'), max_length=32)                                         # валюта, UAH|USD|EUR&
    details = models.CharField(_('details'), max_length=128)                                # назначение&
    pay_way = models.CharField(_('pay way'), max_length=32)                                 # privat24&
    order = models.CharField(_('order'), max_length=64, unique=True)                        # order_id, 1&
    merchant = models.CharField(_('merchant'), max_length=64)                               # merchant id, 1&
    state = models.CharField(_('state'), max_length=32)                                     # ок|fail|test&
    date = models.CharField(_('date'), max_length=64)                                       # 010113232010 (фомат ddMMyyHHmmss)
    signature = models.TextField(_('signature'))                                            # сигнатура
    ext_details = models.CharField(_('ext details'), max_length=255, null=True, blank=True) # расширенное_назначение&
    reference = models.CharField(_('reference'), max_length=64, null=True, blank=True)      # референс
    sender_phone = models.CharField(_('sender phone'), max_length=64, null=True, blank=True)# +380971234567
    raw_data = models.TextField(_('raw data'), null=True, blank=True)

    class Meta:
        verbose_name = _('privat24 transaction')
        verbose_name_plural = _('privat24 transactions')
        abstract = True

    def __unicode__(self):
        return _('Transaction #(%s)') % self.order


class Privat24Transaction(AbstractPrivat24Transaction):

    class Meta:
        swappable = 'PRIVAT24_TRANSACTION_MODEL'
