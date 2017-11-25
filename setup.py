import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'Beaker==1.9.0',
    'beautifulsoup4==4.6.0',
    'bs4==0.0.1',
    'certifi==2017.11.5',
    'Chameleon==3.2',
    'chardet==3.0.4',
    'Cython==0.27.3',
    'demjson==2.2.4',
    'hupper==1.0',
    'idna==2.6',
    'jsonpickle==0.9.5',
    'jsonschema==2.6.0',
    'Mako==1.0.7',
    'MarkupSafe==1.0',
    'mock==2.0.0',
    'PasteDeploy==1.5.2',
    'pbr==3.1.1',
    'phpserialize==1.3',
    'plaster==1.0',
    'plaster-pastedeploy==0.4.2',
    'Pygments==2.2.0',
    'PyHamcrest==1.9.0',
    'pyramid==1.9.1',
    'pyramid-beaker==0.8',
    'pyramid-chameleon==0.3',
    'pyramid-debugtoolbar==4.3',
    'pyramid-mako==1.0.2',
    'pyramid-tm==2.2',
    'repoze.lru==0.7',
    'requests==2.18.4',
    'six==1.11.0',
    'SQLAlchemy==1.1.15',
    'transaction==2.1.2',
    'translationstring==1.3',
    'urllib3==1.22',
    'venusian==1.1.0',
    'waitress==1.1.0',
    'WebOb==1.7.4',
    'WebTest==2.0.29',
    'zope.deprecation==4.3.0',
    'zope.interface==4.4.3',
    'zope.sqlalchemy==0.7.7',
    'https://launchpad.net/oursql/py3k/py3k-0.9.4/+download/oursql-0.9.4.zip',
]

setup(
    name='Pynformatics',
    version='0.0',
    description='Pynformatics',
    long_description=README + '\n\n' +  CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web wsgi bfg pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='pynformatics',
    install_requires=requires,
    entry_points="""
        [paste.app_factory]
        main = pynformatics:main
        [console_scripts]
        populate_Pynformatics = pynformatics.scripts.populate:main
    """,
)