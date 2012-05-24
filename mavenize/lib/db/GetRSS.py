import AlchemyAPI,re,urllib2
from bs4 import BeautifulSoup as soup
class GetRSS:
    print('Imported script successfully.');
    def __init__(self):
        self.alchemyObject = AlchemyAPI.AlchemyAPI()
        self.alchemyObject.loadAPIKey("mavenize/lib/db/api_key.txt")
        print('Key loaded successfully.')
        #Provided a sample URL, in case you want to test it
        self.url = 'http://www.rottentomatoes.com/syndication/rss/top_news.xml'
        print('Script loaded sucessfully.')
    
    def getPermaLinks(self,url):
        print('called helper method')
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        page = urllib2.urlopen(req) #We are blocked from accessing feeds (detected as bot)
        #I foresee the above being large-scale inefficient.  Any ideas?
        soupPage = soup(page)
        returnList = []
        unparsedList = soupPage.findAll('guid')
        if not unparsedList: #Some RSS pages use the 'link' tag rather than the 'guid' tag
            unparsedList = soupPage.findAll('link')
        for listelement in unparsedList:
	        returnList.append(listelement.findAll(text=True)[0].encode('ascii'))
        return returnList

    def getLumpText(self,url): #We strip the navigation links and get only content.
        #Should we leave in \n and \t marks, or no?
        print('Getting Lump Text');
        returnText = self.alchemyObject.URLGetText(url)
        return returnText

    def getAuthor(self, url):#Works for some, not for others.
        rawReturn =  self.alchemyObject.URLGetAuthor(url)
        souped = soup(rawReturn)
        rawAuthor = souped.findAll('author')[0]
        return rawAuthor.findAll(text=True)[0].encode('ascii')

    def getMovieTitle(self,text):
        rawEntities = self.alchemyObject.TextGetRankedNamedEntities(text)
        return rawEntities

    def getSummaryText(self,url):
        pass #We want either the first or last paragraph

    def getSentimentFromText(self, text):# Will feed this from output of the getLumpText function
        rawReturn =  self.alchemyObject.TextGetTextSentiment(text)
        souped = soup(rawReturn)
        
        rawState = souped.findAll('type')[0]
        state = rawState.findAll(text=True)[0].encode('ascii')
        print('the type is ' + state)

        if not (state == 'positive' or state == 'negative'):
            return 0 #what do I do when the state is neutral?
        else:
            rawScore = souped.findAll('score')[0]
            score = rawScore.findAll(text=True)[0].encode('ascii')
            return float(score)#This returns a number -1.0 to 1.0
        #We should base our rating system off the collective entirety of every review in our system
        #i.e. take an average of all the sentiment values, let rating of 3 be the mean value
        #rating of 4 to be one  quartile and above
        #rating of 2 to be one quartile below


        
        return souped
    def getP(self,url):
        rawReturn = self.alchemyObject.URLGetText(url)
        rawReturn = rawReturn.replace('\t','')
        rawReturn = rawReturn.replace('  ',' ')
        souped = soup(rawReturn)
        text = souped.findAll('text')
        strippedText =  text[0].findAll(text=True)[0].encode('ascii','ignore')
        occurances = self.getOccurances(strippedText,"\n")
        startIndex = occurances[len(occurances) - 3]
        summary = strippedText[startIndex:]
        summary = summary.replace('\n','')
       # summary = summary.replace('\'',"") #I assume you don't want to get rid
       # of this type of grammar
        return summary

    def getOccurances(self,text,findstring):
         return [match.start() for match in re.finditer(re.escape(findstring), text)]
        

