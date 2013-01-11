# Net Portal 2.0

Replacement for Waseda Net Portal to get a usable interface.
Only the Course Navi module is being developed at the present. Other modules will come later.

## Local install
### Dependencies
* Python 2
* Django 1.4
* Psycopg 2 (Python 2)
* Python 3 (for installation script)
* BeautifulSoup4 (Python 3)

### Installation
Run

    python3 scripts/parse_subjects.py

Check the database settings in `src/net_portal/settings.py` and sync the database

    python2 src/manage.py syncdb
