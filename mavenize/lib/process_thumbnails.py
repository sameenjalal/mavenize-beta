from movie.models import Movie
from sorl.thumbnail import get_thumbnail

for movie in Movie.objects.all():
    try:
        get_thumbnail(movie.image, 'x285')
    except Exception, e:
        print "Error processing Movie ID: %s" % (str(movie.pk))
        print e
