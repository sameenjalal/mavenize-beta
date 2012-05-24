from movie.models import Movie
import urllib as urllib
import urllib2,json

author_list = []

BASE='http://api.rottentomatoes.com/api/public/v1.0/'
KEY='mz7z7f9zm79tc3hcaw3xb85w'
def main():
    print('starting.')
    checkStrSet = set([])
    for movie in Movie.objects.order_by("-theater_date"):
        print('Getting reviews for movie '+movie.title)
        singlemoviereviews  = getAuthors(movie)
        for review in singlemoviereviews:
            checkStr = review['critic'][0:5]+review['link'][7:14]
            print('checkStr is '+ checkStr)
            if not checkStr in checkStrSet:
                author_list.append(tempset)
                print('Successfully added author set for'+movie.tite)
                checkStrSet.add(checkStr)
def getAuthors(movie):
    print('Get authors from'+movie.title)
    title = movie.title
    imdb_id = movie.imdb_id
    #PROBLEM HERE DOEES NOT GET reviewDATA ARRAY
    reviewSearchURL=BASE+'movies/'+str(imdb_id)+'/reviews.json?'

    reviewSearchURL = reviewSearchURL+urllib.urlencode({'apikey':KEY})
    print('Search url is ' + reviewSearchURL)
    reviewData=json.loads(urllib2.urlopen(reviewSearchURL).read())
    reviewData = reviewData['reviews']
    print('Printing reviewData')
    print(reviewData)
    returnSet=[]
    for review in reviewData:
        returnSet.append({'author':review['critic'],
        'link':review['links']['review']})
    return returnSet

        #tempset now an array of dictionaries that contain
        #author and url
        #Check whether author and url combination exists
        #If found duplicate, set addMovie to false

        #We want to have one url for each unique author
