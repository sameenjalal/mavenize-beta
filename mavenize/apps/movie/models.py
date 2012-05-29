from django.db import models
from django.template.defaultfilters import slugify
from item.models import Item
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Genre(models.Model):
    name = models.CharField(max_length=255)
    url = models.SlugField(null=True, blank=True, max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

class Actor(models.Model):
    name = models.CharField(max_length=255)
    url = models.SlugField(null=True, blank=True, max_length=255)
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.name)
        super(Actor, self).save(*args, **kwargs)

class Director(models.Model):
    name = models.CharField(max_length=255)
    url = models.SlugField(null=True, blank=True, max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.name)
        super(Director, self).save(*args, **kwargs)

class Movie(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    imdb_id = models.IntegerField()
    title = models.CharField(max_length=255)
    keywords = models.TextField()
    runtime = models.SmallIntegerField()
    synopsis = models.TextField()
    theater_date = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to='img/movies',
        default='img/movies/default.jpg',
        max_length=255
    )
    genre = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor)
    url = models.SlugField(null=True, blank=True, max_length=255)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.item_id:
            self.item = Item.objects.create(item_type='movie')
            self.url = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

@receiver(post_delete, sender=Movie)
def delete_movie(sender, instance, **kwargs):
    Item.objects.get(pk=instance.pk).delete()
