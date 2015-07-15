#Josiah patron accounts

This is exploratory code in an attempt to allow [Josiah](http://josiah.brown.edu/) patron account features in another application - easyArticle, VuFind, Blacklight, etc.


## Development

* Uses [py.test](http://pytest.org/latest/)

* Example py.test usage:

    `py.test ./test_account.py` -- runs all tests

    `py.test -s ./test_account.py` -- displays log output

    `py.test -v ./test_account.py` -- verbose

    `py.test ./test_account.py::test_place_hold_annex` -- runs single test

* [vcrpy](https://github.com/kevin1024/vcrpy) is used to generate test fixtures.  These are not stored in the repository to protect possible sensitive information.  They can be regenerated following the vcrpy documentation.  Brown Univ developers can contact [@birkin](https://github.com/birkin) to obtain Brown-specific test fixtures.


## Issues and ToDos

 * Test with various user types (student, grad student, faculty, etc)

 * Test various types of requests; some types/locations may require a differing posted payloads.

---
