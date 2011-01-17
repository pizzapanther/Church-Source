# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Setting'
        db.create_table('configuration_setting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('skey', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=75, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stype', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal('configuration', ['Setting'])


    def backwards(self, orm):
        
        # Deleting model 'Setting'
        db.delete_table('configuration_setting')


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
