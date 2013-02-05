# Net Portal 2.0

Replacement for Waseda Net Portal to get a usable interface.
Only the Course Navi module is being developed at the present. Other modules will come later.

## Local install
### Dependencies
As Django does not support Python 3 yet, all the code are written in Python 2.

* [Python 2](http://www.python.org/download/)
* [Django 1.4](https://www.djangoproject.com/download/) ``pip install Django``
* [Psycopg 2](http://pypi.python.org/pypi/psycopg2) ``pip install psycopg2``
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) ``pip install beautifulsoup4``
* [lxml 2.3](http://lxml.de/index.html#download) ``pip install lxml``
* [python-rsa 3](http://stuvel.eu/files/python-rsa-doc/installation.html) ``pip install rsa``
* [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar) ``pip install django-debug-toolbar``


### Installation
The dependencies can be installed automatically by running.

    python2 setup.py develop

`libxml2-dev` and `libxslt1-dev` are required to build `lxml`. If you prefer, you can look for lxml binary directly.
Postgresql needs to be installed and `pg_config` available on the path for psycopg2 to be installed properly.
If you get an error with HTTPS while installing Django, try to install it via `pip`.

Once all the dependencies are installed, run

    python2 scripts/generate_keys.py OUTPUT_DIR

to generate RSA keys to use in the program. OUTPUT_DIR can be any directory (existing or not) name where you have write access.

Then, check the database settings in `src/django_app/net_portal/settings.py` and run

    python2 scripts/reset_all.py

This will generate the initial data from the gzipped HTML, synchronize the database and add the initial data to the database.
The process may take a long time (between 3 and 10 minutes depending on your machine) so be patient.
You can safely answer 'no' when you will be asked if you want to create an admin user.

Once this is done, you should then be able to run the Django application normally by running

    python2 src/django_app/manage.py runserver PORT

