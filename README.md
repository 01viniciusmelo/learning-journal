[![Build Status](https://travis-ci.org/benpetty/Learning-Journal.svg?branch=master)](https://travis-ci.org/benpetty/Learning-Journal) [![Coverage Status](https://coveralls.io/repos/github/benpetty/Learning-Journal/badge.svg?branch=master)](https://coveralls.io/github/benpetty/Learning-Journal?branch=master)

# **Pyramid Learning Journal Project**

***

This repo contains the source code for my personal learning journal—a blog app created in Python using Pyramid's *alchemy* starter scaffold. It is deployed at http://mylearningjournal.herokuapp.com

## Application dependencies:

- `pyramid`
- `pyramid_jinja2`
- `pyramid_tm`
- `SQLAlchemy`
- `transaction`
- `zope.sqlalchemy`
- `waitress`
- `markdown`
- `bleach`
- `psycopg2`
- `passlib`

## Development

To get started with your own version of this application:
```bash
# 1. Clone this repo.
# 2. Initialize/activate your virtual environment with variable declarations.
# 3. Install all the required packages, including testing:
$ pip install -e .[testing]
# 4. Create your database with Postgres:
$ createdb learning_journal
# 5. Erase any existing entries and initializes a new database for your local environment:
$ initialize_db development.ini
# 6. Serve the page locally:
$ pserve development.ini --reload
```

When initializing your new database, a default entry is created which you can edit or delete. A default admin user is also initialized with the username `admin` and password `password`. Change this users details through the web app, or edit the corresponding fields in `scripts/initalizedb.py` before deployment.

## Deployment via Heroku

Create your Heroku app with `$ heroku create <your_app_name>`.  Enable Postgres on Heroku with `$ heroku addons:create heroku-postgresql:hobby-dev` (more info and options [here](https://devcenter.heroku.com/articles/heroku-postgresql#create-a-new-database)). To initialize the production database for deployment, open the `run` file in the projects root directory and uncomment out line 4. It should now be:

```
#!/bin/bash
set -e
python setup.py develop
initialize_db production.ini
python runapp.py
```

`$ git add run`, `$ git commit -m 'Initialize server with database.'` and then `$ git push heroku master` will upload the app and initializes the database. Go back to the `run` file and comment out line 4 `# initialize_db production.ini` and repeat the ACP.

## Models

- **Jentry** - A journal entry/blog post. Properties include: 
  - `id` (primary key)
  - `title`
  - `author_username`
  - `content` (can be plain text or Markdown)
  - `contentr` (content after being rendered to HTML)
  - `created` (DateTime object)
  - `modfied` (DateTime object)
  - `category`
- **User** - Application user model. Properties include:
  - `id` (primary key)
  - `username`
  - hashed `password`
  - `firstname`
  - `lastname`
  - `email`
  - `bio`
  - `author` privileges (Boolean)
  - `admin` privileges (Boolean)

## Environment Variables

Declare the environment variables `DATABASE_URL` and `AUTH_SECRET`. For example add something like this to your `bin/activate` file for development environment:

```
export DATABASE_URL="postgres://username@localhost:5432/learning_journal"
export AUTH_SECRET="potato"
```

## Testing

### Testing Dependencies

- `pytest`
- `pytest-cov`
- `tox`
- `faker`
- `WebTest`

## Credits

by [Ben Petty](https://github.com/benpetty). Borrows much from [Expense Tracker](https://github.com/nhuntwalker/expense_tracker) by Nicholas Hunt-Walker, my instructor.