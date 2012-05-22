# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('user_profile_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(default='img/users/avatars/default.jpg', max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='img/users/thumbnails/default.jpg', max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('about_me', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
        ))
        db.send_create_signal('user_profile', ['UserProfile'])

        # Adding model 'UserStatistics'
        db.create_table('user_profile_userstatistics', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('karma', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reviews', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bookmarks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('agrees_out', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('agrees_in', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('thanks_out', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('thanks_in', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('user_profile', ['UserStatistics'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('user_profile_userprofile')

        # Deleting model 'UserStatistics'
        db.delete_table('user_profile_userstatistics')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'user_profile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'img/users/avatars/default.jpg'", 'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'img/users/thumbnails/default.jpg'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'user_profile.userstatistics': {
            'Meta': {'object_name': 'UserStatistics'},
            'agrees_in': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'agrees_out': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bookmarks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reviews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thanks_in': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thanks_out': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['user_profile']