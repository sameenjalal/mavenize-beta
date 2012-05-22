from urllib2 import urlopen, HTTPError
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

from item.models import Item, Link
from movie.models import Movie, Actor, Director, Genre
from decorators.retry import retry

class LoadMovie():
    """
    This manager inserts a movie into the database along with its
    corresponding genres, actors, and directors.
    """
    exists = False
    
    def __init__(self, title, imdb_id, runtime,
                 synopsis, theater_date, keywords):
        """
        Inserts the movie into the database if it doesn't already
        exist in the database.
        """
        self.movie, self.created = Movie.objects.get_or_create(
            title=title,
            imdb_id=imdb_id,
            runtime=runtime,
            synopsis=synopsis,
            theater_date=theater_date,
            keywords = keywords,
            url=slugify(title)
        )

    def insert_genres(self, genres):
        """
        Inserts the genres for the movie.
        """
        genre_list = []
        for g in genres:
            genre, created = Genre.objects.get_or_create(
                name=g, url=slugify(g))
            genre_list.append(genre)
        self.movie.genre.add(*genre_list)

    def insert_actors(self, actors):
        """
        Inserts the actors for the movie.
        """
        actor_list = []
        for a in actors:
            actor, created = Actor.objects.get_or_create(
                name=a, url=slugify(a))
            actor_list.append(actor)
        self.movie.actors.add(*actor_list)

    def insert_directors(self, directors):
        """
        Inserts the directors for the movie.
        """
        director_list = []
        for d in directors:
            director, created = Director.objects.get_or_create(
                name=d, url=slugify(d))
            director_list.append(director)
        self.movie.directors.add(*director_list)

    @retry(HTTPError)
    def insert_image(self, url):
        """
        Inserts the image for the movie.
        """
        if 'default.jpg' in self.movie.image.url:
            image = urlopen(url, timeout=15)
            self.movie.image.save(
                self.movie.url+u'.jpg',
                ContentFile(image.read())
            )

    def insert_trailer(self, url):
        """
        Inserts the trailer as a link.
        """
        Link.objects.get_or_create(
            item=self.movie.item,
            partner="YouTube",
            url=url
        )
