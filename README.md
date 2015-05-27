#Josiah patron accounts

This is exploratory code in an attempt to allow Josiah patron account features in another application - easyArticle, VuFind/Blacklight, etc.  It was written in January 2014.

## Development

Running tests with py.test and showing ouput: `py.test -s`.


##HTML

Sample html files are included in the repo.  These are there to test the parsing.  The HTML was saved in early 2012 but I doubt has changed much. 


##Issues

 * It uses pyquery, probabably better to use BeautifulSoup4 since it has been released in the interim and has proved to be less buggy than pyquery in production.  


##Sample patrons

Bonnie creates sample patrons that can be used for testing requests.  
