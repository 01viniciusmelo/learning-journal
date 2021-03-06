"""Setup."""


import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'ipython',
    'pyramid_ipython',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'markdown',
    'bleach',
    'psycopg2',
    'passlib',
]

tests_require = [
    'pytest',
    'pytest-cov',
    'tox',
    'faker',
    'coveralls',
    'WebTest',
]

setup(name='learning_journal',
      version='0.0',
      description='learning_journal',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Benjamin Petty',
      author_email='contact@benpetty.me',
      url='benpetty.me',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = learning_journal:main
      [console_scripts]
      initialize_db = learning_journal.scripts.initializedb:main
      """,
      )
