import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'bs4',
    'mysqlclient',
    'demjson',
    'jsonpickle',
    'phpserialize',
    'requests',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_boto3',
    'SQLAlchemy==1.4.53',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='Pynformatics',
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
      entry_points="""\
      [paste.app_factory]
      main = pynformatics:main
      [console_scripts]
      populate_Pynformatics = pynformatics.scripts.populate:main
      """,
      )

