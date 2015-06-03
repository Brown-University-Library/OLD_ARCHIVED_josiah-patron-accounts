#Josiah patron accounts

This is exploratory code in an attempt to allow [Josiah](http://josiah.brown.edu/) patron account features in another application - easyArticle, VuFind, Blacklight, etc.

## Development

Running tests with py.test and showing ouput: `py.test -s`.

[vcrpy](https://github.com/kevin1024/vcrpy) is used to generate test fixtures.  These are not stored in the repository to protect possible sensitive information.  They can be regenerated following the vcrpy documentation.  Brown Univ developers should contact [@birkin](https://github.com/birkin) to obtain a Brown specific test fixtures.


##Issues and ToDos

 * HTML parsing is currently done with pyquery.  This will be replaced with [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4).
 * Test with various user types (student, grad student, faculty, etc)
