from movie.models import Movie
from sorl.thumbnail import get_thumbnail
from celery import task

def cache_thumbnails():
    num_movies = Movie.objects.all().count()
    per_section = num_movies / 12
    indexes = range(0, num_movies, per_section)
    for i in range(len(indexes))[:-1]:
        cache_subset.delay(indexes[i], indexes[i+1])


@task(ignore_result=True)
def cache_subset(start, end, callback=None)
    for movie in Movie.objects.all()[start:end]:
        try:
            get_thumbnail(movie.image, 'x285')
        except Exception, e:
            print "Error processing Movie ID: %s" % (str(movie.pk))
            print e
