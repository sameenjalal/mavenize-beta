from movie.models import Movie
from sorl.thumbnail import get_thumbnail

for movie in Movie.objects.all():
    try:
        get_thumbnail(movie.image, 'x285')
    except IOError:
        print movie.pk
