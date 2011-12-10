# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CheckIn.printed'
        db.add_column('check_in_checkin', 'printed', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CheckIn.printed'
        db.delete_column('check_in_checkin', 'printed')


    models = {
        'check_in.checkin': {
            'Meta': {'ordering': "('-cin', 'person__lname', 'person__fname')", 'object_name': 'CheckIn'},
            'cin': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'cout': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['check_in.Event']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pager': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'printed': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'check_in.event': {
            'Meta': {'ordering': "('-start', 'name')", 'object_name': 'Event'},
            'code': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['check_in.Event']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'check_in.eventgroup': {
            'Meta': {'ordering': "('group', 'room')", 'object_name': 'EventGroup'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['check_in.Event']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resources.Room']", 'null': 'True', 'blank': 'True'})
        },
        'people.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gtype': ('django.db.models.fields.CharField', [], {'default': "'general'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'people.household': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Household'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anniversary': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_visit': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_temp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.TempImage']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ns'", 'max_length': '10'})
        },
        'people.person': {
            'Meta': {'ordering': "('lname', 'fname')", 'object_name': 'Person'},
            'alerts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allergies': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ddate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'ns'", 'max_length': '10'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['people.Group']", 'null': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Household']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_temp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.TempImage']", 'null': 'True', 'blank': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'mname': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'ns'", 'max_length': '10'})
        },
        'people.tempimage': {
            'Meta': {'ordering': "('-ts',)", 'object_name': 'TempImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'resources.room': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Room'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['check_in']
