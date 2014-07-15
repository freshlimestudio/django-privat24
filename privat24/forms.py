# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from django import forms
import sys
from hashlib import md5, sha1
import base64

from OpenSSL import crypto

from privat24 import models

class Privat24Form(forms.Form):
    amt = forms.DecimalField()


class Privat24FrontForm(Privat24Form):
    amt = forms.DecimalField(widget=forms.TextInput())
    ccy = forms.CharField(widget=forms.TextInput())
    merchant= forms.CharField(widget=forms.HiddenInput())
    order= forms.CharField(widget=forms.HiddenInput())
    details= forms.CharField(widget=forms.HiddenInput())
    pay_way= forms.CharField(widget=forms.HiddenInput())
    return_url= forms.CharField(widget=forms.HiddenInput())
    server_url= forms.CharField(widget=forms.HiddenInput())
    ext_details= forms.CharField(widget=forms.HiddenInput(), required=False)

class Privat24BackForm(Privat24Form):

    def __init__(self, integration, *args, **kwargs):
        self.integration = integration
        super( Privat24BackForm, self).__init__(*args, **kwargs)

    amt = forms.DecimalField()
    ccy = forms.ChoiceField(choices=models.P24_CCY_CHOICES)
    merchant= forms.CharField()
    order= forms.CharField()
    details= forms.CharField()
    pay_way= forms.CharField()
#    state = forms.ChoiceField(choices=models.P24_STATE_CHOICES)
    state = forms.CharField()
    date = forms.CharField()
    ext_details= forms.CharField(required=False)
    reference = forms.CharField(required=False)
    sender_phone = forms.CharField(required=False)
