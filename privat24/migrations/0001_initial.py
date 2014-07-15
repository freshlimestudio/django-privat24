# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Privat24Transaction'
        db.create_table(u'privat24_privat24transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amt', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('ccy', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('ext_details', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pay_way', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('merchant', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('sender_phone', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('raw_data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('signature', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'privat24', ['Privat24Transaction'])


    def backwards(self, orm):
        # Deleting model 'Privat24Transaction'
        db.delete_table(u'privat24_privat24transaction')


    models = {
        u'privat24.privat24transaction': {
            'Meta': {'object_name': 'Privat24Transaction'},
            'amt': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'ccy': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'ext_details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pay_way': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sender_phone': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['privat24']