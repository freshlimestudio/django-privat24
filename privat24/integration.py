import datetime
import time
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from hashlib import md5, sha1
import urlparse

from .conf import get_options
from .forms import Privat24BackForm, Privat24FrontForm
from . import models
import logging
from django.utils.encoding import force_unicode

from .signals import transaction_was_successful

csrf_exempt_m = method_decorator(csrf_exempt)
never_cache_m = method_decorator(never_cache)
require_POST_m = method_decorator(require_POST)

from . import get_privat24_transaction_model
TransactionModel = get_privat24_transaction_model()

logger = logging.getLogger('app')

class Privat24Integration(object):

    # The mode of the gateway. Looks into the settings else
    # defaults to True
#    test_mode = get_ukrpays_constant("test_mode")
    display_name = "Privat24"

    def __init__(self, options=None):
        # read settings options
        settings_options = get_options()
        if not options:
            options = {}
        settings_options.update(options)
        # The form fields that will be rendered in the template
        self.fields = {}
        self.fields.update(settings_options)
        self._form_class = Privat24FrontForm

        if self.fields:
            self.amt = self.fields.get("amt")
            self.ccy = self.fields.get("ccy")
            self.order = self.fields.get("order")
            self.details = self.fields.get("details")
            self.ext_details = self.fields.get("ext_details")
            self.pay_way = self.fields.get("pay_way")
            self.merchant = self.fields.get("merchant")
            self.password = self.fields.get("password")
            self.return_url = self.fields.get("return_url")
            self.server_url = self.fields.get("server_url")
            if not self.merchant:
                raise ImproperlyConfigured("Option PRIVAT24_OPTIONS['merchant'] must be set in your settings.py file.")
            if not self.password:
                raise ImproperlyConfigured("Option PRIVAT24_OPTIONS['password'] must be set in your settings.py file.")
            if not self.return_url:
                raise ImproperlyConfigured("Option PRIVAT24_OPTIONS['return_url'] must be set in your settings.py file.")
            _form_class = self.fields.get("form_class")
            if _form_class:
                self._form_class = _form_class

    def add_field(self, key, value):
        self.fields[key] = value

    def add_fields(self, params):
        for (key, val) in params.iteritems():
            self.add_field(key, val)

    def form_class(self):
        return self._form_class

    def get_urls(self):
        urlpatterns = patterns('',
           url(r'^notify-handler/$', self.privat24_notify_handler, name="privat24_notify_handler"),
        )
        return urlpatterns

    def build_signature(self, payment):
        test_str = ("%s%s" % (payment.encode('utf-8'), self.password))
        return sha1(md5(test_str).hexdigest()).hexdigest()

    def handle_request(self, request):
        payment = request.POST.get('payment')
        signature =request.POST.get('signature')
        result = 'FAIL'
        local_signature = self.build_signature(payment)

        logger.info("POST: %s" % request.POST)
        logger.info("payment: %s" % payment)
        logger.info("signature: %s" % signature)

        if local_signature == signature:
            params = dict(urlparse.parse_qsl(payment))
            form = Privat24BackForm(self, params)
            if not form.is_valid():
                return ("ERROR %s" % form.errors.as_text()).encode('utf-8')
            else:
                # Apply Changes
                cd = form.cleaned_data
                sum_amt = float(cd['amt'])
                post_data = cd.copy()
                op_date = time.strptime(cd['date'], "%d%m%y%H%M%S")
                post_data['pdate'] = time.strftime('%Y-%m-%d %H:%M:%S', op_date)
                order_id = cd.get('order')
                trans = None
                try:
                    trans = TransactionModel.objects.get(order=order_id)
                except TransactionModel.DoesNotExist:
                    trans = TransactionModel.objects.create(
                        amt = sum_amt,
                        ccy = cd.get('ccy'),
                        details = cd.get('details'),
                        pay_way = cd.get('pay_way'),
                        order = cd.get('order'),
                        merchant = cd.get('merchant'),
                        state = cd.get('state'),
                        date = cd.get('date'),
                        signature = signature,
                        ext_details = cd.get('ext_details'),
                        reference = cd.get('reference'),
                        sender_phone = cd.get('sender_phone'),
#                        raw_data = request.body,
                    )
                except Exception, e:
                    result = e.message.encode('utf-8')
                if trans:
                    post_data['local_trans_id'] = trans.pk
                    post_data['request'] = request
                    transaction_was_successful.send(sender=self.__class__,
                        type="purchase",
                        response=post_data
                    )
                    result = 'OK'
        return result


    @csrf_exempt_m
    @never_cache_m
    @require_POST_m
    def privat24_notify_handler(self, request):
        return HttpResponse(self.handle_request(request), content_type="text/xml; charset=UTF-8")

    @property
    def urls(self):
        return self.get_urls()

    def generate_tr_data(self):
        tr_data = {
            'merchant': self.merchant,
            'pay_way': self.pay_way,
            'return_url': self.return_url,
            'server_url': self.server_url,
        }
        if  self.server_url:
            tr_data['server_url'] = self.server_url
        return tr_data

    @property
    def service_url(self):
#        if self.test_mode:
#            return 'https://api.privatbank.ua/p24api/ishop'
        return 'https://api.privatbank.ua/p24api/ishop'

    def generate_form(self):
        initial_data = self.generate_tr_data()
        initial_data.update(self.fields)
        form = self.form_class()(initial=initial_data)
        return form
