# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from churchsource.configuration.models import Setting

class Migration(DataMigration):
    def forwards(self, orm):
        s1 = Setting(skey='LOGO', name='Logo shown on check in terminal', stype='str', value='')
        s1.save()
        
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
