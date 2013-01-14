# Net Portal 2.0

Replacement for Waseda Net Portal to get a usable interface.
Only the Course Navi module is being developed at the present. Other modules will come later.

## Local install
### Dependencies
As Django does not support Python 3 yet, all the code are written in Python 2.
* [Python 2](http://www.python.org/download/)
* [Django 1.4](https://www.djangoproject.com/download/)
* [Psycopg 2](http://pypi.python.org/pypi/psycopg2)
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [lxml 3](http://lxml.de/index.html#download)
* [python-rsa 3](http://stuvel.eu/files/python-rsa-doc/installation.html)
* [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)

### Installation
Run

    python2 scripts/parse_subjects.py

to generate the initial database data (it may take a while) and

    python2 scripts/generate_keys.py

to generate RSA keys to use in the program.

Check the database settings in `src/net_portal/settings.py` and sync the database by running

    python2 src/manage.py syncdb
