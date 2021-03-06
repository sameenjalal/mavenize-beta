#!/usr/bin/python

import os
from sys import argv, exit
import json
import datetime

from db.loadmovie import LoadMovie

usage = '''Usage:   %s DIR

SRCDIR should have files containing JSON data for TMDb movies. Each file
should contain only movie or error message. '''

MOVIE_ITEM_TYPE = 1

srcdir = None

def main(inputdir):
    global srcdir
    if len(argv) < 1:
        print usage % argv[0]
        exit(0)

    srcdir = os.path.abspath(inputdir)

    if os.path.exists(srcdir) == False:
        print 'Error: %s doesn\'t exists or unreachable.' % srcdir
        exit(1)

    process_dir(srcdir)

def process_dir(directory):
    ls = os.listdir(directory)
    for f in ls:
        path = os.path.join(directory, f)
        if os.path.isfile(path):
            process_file(path)

def process_file(path):
    contents = None

    try:
        f = open(path, 'r')
        contents = f.read()
        f.close()
    except IOError as e:
        print 'IOError occurred: %s' % e
        exit(1)

    process_file_content(contents, path)

def process_file_content(content, filename):
    '''Process json content, ignore errors, save to db.'''
    movie = prepare_from_json(content,filename)

    if movie != None:
        save_movie(movie)


def prepare_from_json(json_str, filename):
    '''Prepare a movie dict from given json str, may return None'''
    try:
        try:
            obj = json.loads(json_str);
            if type(obj) is list:
                obj = obj[0]

            if type(obj) in [unicode, str]:
                #print 'File %s is not json object.' % filename
                return

            if obj['movie_type'] != 'movie':
                return
            if obj['language'] != 'en':
                return

            # our movie object
            movie = {
                    'type' : obj['movie_type'], #should be movie
                    'tmdb_id': obj['id'],
                    'popularity' : obj['popularity'],
                    }

            name_keys = ['name', 'original_name', 'alternative_name']
            names = []
            ins_name_obj = {}

            for name_key in name_keys:
                if name_key in obj and not obj[name_key] in names:
                    name = obj[name_key]
                    if name != None:
                        names.append(obj[name_key])
                        ins_name_obj[name_key] = obj[name_key]

            movie['names'] = ins_name_obj

            """
            print "PRINTING OBJ -- BEG"
            print obj.keys()
            print obj.values()
            print "PRINTING OBJ -- END"
            """
            if 'released' in obj: movie['released'] = obj['released']
            if 'overview' in obj: movie['overview'] = obj['overview']
            if 'certification' in obj: movie['certification'] = obj['certification']
            if 'keywords' in obj: movie['keywords'] = obj['keywords']
            if 'votes' in obj: movie['votes'] = obj['votes']
            if 'rating' in obj: movie['rating'] = obj['rating']
            if 'runtime' in obj: movie['runtime'] = obj['runtime']
            if 'trailer' in obj: movie['trailer'] = obj['trailer']
            if 'imdb_id' in obj: movie['imdb_id'] = obj['imdb_id']
            if 'tagline' in obj: movie['tagline'] = obj['tagline']
            if 'revenue' in obj: movie['revenue'] = obj['revenue']
            if 'language' in obj: movie['language'] = obj['language']
            if 'genres' in obj and obj['genres'] != []:
                names = []
                for genre in obj['genres']:
                    names.append(genre['name'])
                movie['genres'] = names

            if 'cast' in obj and obj['cast'] != []:
                names = []
                all_cast = []
                for cast in obj['cast']:
                    if (not cast['name'] in names):
                        # avoid duplicate cast
                        names.append(cast['name'])
                        one_cast = {
                            'name': cast['name'],
                            'character': cast['character'],
                            'job': cast['job'],
                            'department': cast['department'],
                            'order': cast['order']
                        }
                        all_cast.append(one_cast)
                names = names[:3]
                movie['cast'] = all_cast

            if 'posters' in obj and obj['posters'] != []:
                pic_url_size_objs = []
                for pic in obj['posters']:
                    img = pic['image']
                    if 'type' in img:
                        if img['type'] == 'poster' and \
                           img['size'] in ['thumb', 'mid', 'original'] and \
                           len(pic_url_size_objs) < 3: # only one poster set
                            # here we trust that imgs will come in sorted order
                            pic_obj = {
                                'url': img['url'],
                                'size': img['size']
                            }
                            pic_url_size_objs.append(pic_obj)
                    movie['pictures'] = pic_url_size_objs

            return movie

        except KeyError as err:
            print 'JSON error in file %s: %s' % (filename, err)
            return

    except ValueError as err:
        print 'Parse error: %s' % err
        return

def save_movie(movie):
    # FILL IN WITH PRINT STATEMENTS
    #print "These are movie keys passed on -- BEG"
   # instance=LoadMovie(
    #    movie[''],
    print('Adding movie '+ movie['names']['name'])

    try:
        keywordstring = ''
        for keyword in movie['keywords']:
            keywordstring = keywordstring + keyword + ','
        imdb = movie['imdb_id'][2:]
        instance = LoadMovie(
            title=movie['names']['name'],
            imdb_id=imdb,
            runtime=movie['runtime'],
            synopsis=movie['overview'],
            theater_date=movie['released'],
            keywords=keywordstring,
        )
        print('...loaded movie')
        #Inserting via LoadMovie helper methods
        #Genres, Directors, Actors, and then Images
        instance.insert_genres(movie['genres'])
        print('...loaded genres')
        #Sort into two arrays of actors and directors
        actors = []
        directors = []
        for person in movie['cast']:
            if (person['job'] == 'Actor') and (person['department'] == 'Actors'):
                actors.append(person['name'])
            elif (person['job'] == 'Director') and (person['department'] == 'Directing'):
                directors.append(person['name'])
        #Call methods to add actors and directors
        instance.insert_actors(actors)
        instance.insert_directors(directors)
        print('...loaded actors & directors')


        #insert_image only takes one image at a time, so traverse movie['pictures']
        if len(movie['pictures']) != 0:
            foundMid = False
            tempLargeImg = {}
            for image in movie['pictures']:
                if image['size']=='mid':
                    instance.insert_image(image['url'])
                    foundMid = True
                elif image['size']=='original':
                    tempLargeImg = image
            if foundMid == False:
                instance.insert_image(tempLargeImg['url'])
            print('...loaded image')
        else:
            print('...no pictures')

        print(movie['trailer'])
        if type(movie['trailer']) != type(None):
            if movie['trailer'].find('youtube') != -1:
                instance.insert_trailer(movie['trailer'])
                print('...loaded trailer')
            else:
                print('Not a YouTube link, did not insert.')
        else:
            print('No trailer link available.')
        print('Sucessfully loaded movie ' + movie['names']['name'])
    except Exception, e:
        print e
        
    # print movie.keys()

    #create an instance of each movie using LoadMovie(...)
    #print movie.values()
    #print "These are movie keys passed on -- END"

if __name__ == '__main__':
    main()

