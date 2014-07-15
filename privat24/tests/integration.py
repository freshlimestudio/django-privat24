# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.html import strip_spaces_between_tags
from django.template import Template, Context
from django.conf import settings
from django.test.utils import override_settings
from urllib import urlencode

#from ..models  import UP_ENCODING_MD5, UP_ENCODING_SHA1
from ..integration import Privat24Integration

from .. import get_privat24_transaction_model
TransactionModel = get_privat24_transaction_model()

class Privat24IntegrationTestCase(TestCase):

    def testFormGen(self):
        p24 = Privat24Integration()
        fields = {
            "amt": "20.00",
            "ccy": "UAH",
            "order": "222",
            "details": "Сплата за питання: Короткий змист тестового питання",
        }
        p24.add_fields(fields)

        tmpl = Template("{% load privat24_form from privat24_tags %}{% privat24_form obj %}")
        form = tmpl.render(Context({"obj": p24}))
        pregen_form = u"""<form method="post" action="https://api.privatbank.ua/p24api/ishop"><p><label for="id_amt">Amt:</label><input id="id_amt" name="amt" type="text" value="20.00" /></p><p><label for="id_ccy">Ccy:</label><input id="id_ccy" name="ccy" type="text" value="UAH" /><input id="id_merchant" name="merchant" type="hidden" value="100000" /><input id="id_order" name="order" type="hidden" value="222" /><input id="id_details" name="details" type="hidden" value="\u0421\u043f\u043b\u0430\u0442\u0430 \u0437\u0430 \u043f\u0438\u0442\u0430\u043d\u043d\u044f: \u041a\u043e\u0440\u043e\u0442\u043a\u0438\u0439 \u0437\u043c\u0438\u0441\u0442 \u0442\u0435\u0441\u0442\u043e\u0432\u043e\u0433\u043e \u043f\u0438\u0442\u0430\u043d\u043d\u044f" /><input id="id_pay_way" name="pay_way" type="hidden" value="privat24" /><input id="id_return_url" name="return_url" type="hidden" value="http://example.com/payments/" /><input id="id_server_url" name="server_url" type="hidden" value="http://example.com/p24/notify-handler/" /><input id="id_ext_details" name="ext_details" type="hidden" /></p></form>"""
        self.assertEquals(pregen_form, strip_spaces_between_tags(form).strip())

    def testNotifyHandlerURLSetup(self):
        self.assertEquals(reverse('privat24_notify_handler'), "/p24/notify-handler/")

    def test_notify_handler(self):
        data = {
            'payment': u'amt=200.00&ccy=UAH&details=\u0421\u043f\u043b\u0430\u0442\u0430 \u0437\u0430 \u043f\u0438\u0442\u0430\u043d\u043d\u044f: \u0422\u0435\u0441\u0442\u043e\u0432\u0435 \u043f\u0438\u0442\u0430\u043d\u043d\u044f&ext_details=&pay_way=privat24&order=1&merchant=100000&state=test&date=160114183814&ref=test payment&sender_phone=+380888888888&payCountry=UA',
            'signature': '7df61c288b9245cf8d1d021256fa4074646ec7de',
        }
        records = TransactionModel.objects.all()
        self.assertEqual(len(records),0)
        resp = self.client.post(reverse('privat24_notify_handler'), data=data)
#        print("-------------------\n%s\n-------------------\n" %resp)
        self.assertEqual(resp.content, 'OK')
        records = TransactionModel.objects.all()
        self.assertEqual(len(records),1)

    def test_notify_handler_with_invalid_data(self):
        data = {
            'payment': u'amt=2000.00&ccy=UAH&details=\u0421\u043f\u043b\u0430\u0442\u0430 \u0437\u0430 \u043f\u0438\u0442\u0430\u043d\u043d\u044f: \u0422\u0435\u0441\u0442\u043e\u0432\u0435 \u043f\u0438\u0442\u0430\u043d\u043d\u044f&ext_details=&pay_way=privat24&order=1&merchant=100000&state=test&date=160114183814&ref=test payment&sender_phone=+380888888888&payCountry=UA',
            'signature': '7df61c288b9245cf8d1d021256fa4074646ec7de',
        }
        resp = self.client.post(reverse('privat24_notify_handler'), data=data)
        self.assertEqual(resp.content, 'FAIL')
