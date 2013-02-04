from setuptools import setup, find_packages

setup(
    name='net-portal',
    version='0.0.1',
    description='A replacement for Waseda Net Portal',
    long_description=open('README.md').read(),
    author='Daniel Perez',
    author_email='tuvistavie@gmail',
    url='https://github.com/tuvistavie/net-portal',
    download_url='https://github.com/tuvistavie/net-portal/archive/master.zip',
    license='WTFPL',
    scripts=['scripts/parse_subjects.py', 'scripts/generate_keys.py', 'scripts/reset_all.py'],
    packages=find_packages("src/django_app"),
    package_dir={'': 'src/django_app'},
    install_requires=[
        'django>=1.3,<1.5',
        'psycopg2',
        'beautifulsoup4',
        'lxml==2.3',
        'rsa',
        'django-debug-toolbar',
        'pyasn1'
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
