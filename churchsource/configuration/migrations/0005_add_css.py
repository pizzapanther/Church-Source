# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from churchsource.configuration.models import Setting

class Migration(DataMigration):

    def forwards(self, orm):
        s1 = Setting(skey='PRINT_CSS', name='CSS used for print label', stype='str', value='css/print.css')
        s1.save()
        
        s2 = Setting(skey='SCREEN_CSS', name='CSS used for check in screen', stype='str', value='css/default.css')
        s2.save()
        
    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'configuration.setting': {
            'Meta': {'ordering': "('skey',)", 'object_name': 'Setting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'skey': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'stype': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['configuration']
