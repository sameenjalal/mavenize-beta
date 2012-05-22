# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table('item_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_type', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('four_star', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('three_star', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('two_star', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('one_star', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reviews', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bookmarks', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('item', ['Item'])

        # Adding model 'Link'
        db.create_table('item_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['item.Item'])),
            ('partner', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('item', ['Link'])

        # Adding model 'Popularity'
        db.create_table('item_popularity', (
            ('item', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['item.Item'], unique=True, primary_key=True)),
            ('today', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('week', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('month', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('alltime', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal('item', ['Popularity'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table('item_item')

        # Deleting model 'Link'
        db.delete_table('item_link')

        # Deleting model 'Popularity'
        db.delete_table('item_popularity')


    models = {
        'item.item': {
            'Meta': {'object_name': 'Item'},
            'bookmarks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'four_star': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'one_star': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reviews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'three_star': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two_star': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'item.link': {
            'Meta': {'object_name': 'Link'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['item.Item']"}),
            'partner': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'item.popularity': {
            'Meta': {'object_name': 'Popularity'},
            'alltime': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['item.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'today': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'week': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        }
    }

    complete_apps = ['item']