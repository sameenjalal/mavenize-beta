# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Forward'
        db.create_table('social_graph_forward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('destination_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('social_graph', ['Forward'])

        # Adding model 'Backward'
        db.create_table('social_graph_backward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('destination_id', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('source_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('social_graph', ['Backward'])


    def backwards(self, orm):
        # Deleting model 'Forward'
        db.delete_table('social_graph_forward')

        # Deleting model 'Backward'
        db.delete_table('social_graph_backward')


    models = {
        'social_graph.backward': {
            'Meta': {'object_name': 'Backward'},
            'destination_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'social_graph.forward': {
            'Meta': {'object_name': 'Forward'},
            'destination_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['social_graph']