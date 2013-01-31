from setuptools import setup, find_packages

setup(
    name='net-portal',
    version='0.0.1',
    description='A replacement for Waseda Net Portal',
    long_description=open('README.md').read(),
    author='Daniel Perez',
    author_email='tuvistavie@gmail',
    url='https://github.com/tuvistavie/net-portal',
    download_url='https://github.com/tuvistavie/net-portal',
    license='WTFPL',
    scripts=['scripts/parse_subjects.py'],
    packages=find_packages("src/django_app/"),
    package_dir={'': 'src/django_app/'},
    tests_require=[
        'django>=1.3,<1.5',
        'psycopg2',
        'beautifulsoup4',
        'lxml',
        'rsa',
        'django-debug-toolbar'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: End Users/Desktop',
        'License :: WTFPL',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ],
)
