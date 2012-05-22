# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Genre'
        db.create_table('movie_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('url', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
        ))
        db.send_create_signal('movie', ['Genre'])

        # Adding model 'Actor'
        db.create_table('movie_actor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('url', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
        ))
        db.send_create_signal('movie', ['Actor'])

        # Adding model 'Director'
        db.create_table('movie_director', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('url', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
        ))
        db.send_create_signal('movie', ['Director'])

        # Adding model 'Movie'
        db.create_table('movie_movie', (
            ('item', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['item.Item'], unique=True, primary_key=True)),
            ('imdb_id', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('keywords', self.gf('django.db.models.fields.TextField')()),
            ('runtime', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('synopsis', self.gf('django.db.models.fields.TextField')()),
            ('theater_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='img/movies/default.jpg', max_length=100)),
            ('url', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
        ))
        db.send_create_signal('movie', ['Movie'])

        # Adding M2M table for field genre on 'Movie'
        db.create_table('movie_movie_genre', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['movie.movie'], null=False)),
            ('genre', models.ForeignKey(orm['movie.genre'], null=False))
        ))
        db.create_unique('movie_movie_genre', ['movie_id', 'genre_id'])

        # Adding M2M table for field directors on 'Movie'
        db.create_table('movie_movie_directors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['movie.movie'], null=False)),
            ('director', models.ForeignKey(orm['movie.director'], null=False))
        ))
        db.create_unique('movie_movie_directors', ['movie_id', 'director_id'])

        # Adding M2M table for field actors on 'Movie'
        db.create_table('movie_movie_actors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['movie.movie'], null=False)),
            ('actor', models.ForeignKey(orm['movie.actor'], null=False))
        ))
        db.create_unique('movie_movie_actors', ['movie_id', 'actor_id'])


    def backwards(self, orm):
        # Deleting model 'Genre'
        db.delete_table('movie_genre')

        # Deleting model 'Actor'
        db.delete_table('movie_actor')

        # Deleting model 'Director'
        db.delete_table('movie_director')

        # Deleting model 'Movie'
        db.delete_table('movie_movie')

        # Removing M2M table for field genre on 'Movie'
        db.delete_table('movie_movie_genre')

        # Removing M2M table for field directors on 'Movie'
        db.delete_table('movie_movie_directors')

        # Removing M2M table for field actors on 'Movie'
        db.delete_table('movie_movie_actors')


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
        'movie.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        'movie.director': {
            'Meta': {'object_name': 'Director'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        'movie.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        'movie.movie': {
            'Meta': {'object_name': 'Movie'},
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movie.Actor']", 'symmetrical': 'False'}),
            'directors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movie.Director']", 'symmetrical': 'False'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movie.Genre']", 'symmetrical': 'False'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'img/movies/default.jpg'", 'max_length': '100'}),
            'imdb_id': ('django.db.models.fields.IntegerField', [], {}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['item.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {}),
            'runtime': ('django.db.models.fields.SmallIntegerField', [], {}),
            'synopsis': ('django.db.models.fields.TextField', [], {}),
            'theater_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        }
    }

    complete_apps = ['movie']