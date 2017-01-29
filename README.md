# Pyramid Learning Journal Project

This repo contains the source code for my personal learning journal—a blog app created in Python using Pyramid's "alchemy" starter scaffold. It is deployed at http://mylearningjournal.herokuapp.com

## Application dependencies:

- 'pyramid'
- 'pyramid_jinja2'
- 'pyramid_debugtoolbar'
- 'pyramid_tm'
- 'ipython'
- 'pyramid_ipython'
- 'SQLAlchemy'
- 'transaction'
- 'zope.sqlalchemy'
- 'waitress'
- 'markdown'
- 'bleach'
- 'psycopg2'
- 'passlib'

To get started with your own version of this learning journal:
```bash
# 1. Clone this repo.
# 2. Initialize/activate your virtual environment.
# 3. Install all the required packages, including testing:
$ pip install -e . 
$ pip install -e .[testing]
# 4. Erase any existing entries and initialize a new database for your local environment:
$ initialize_db development.ini
# 5. Serve the page locally.
$ pserve development.ini --reload
```

When initializing your new database, a default entry is created which you can edit or delete. A default super user is also initialized with the username `admin` and password `password`. You can/should change this users details through the web app itself or edit the fields before initialization in `scripts/initalizedb.py`

## Deployment via Heroku

Create your Heroku app with `$ heroku create <your_app_name>`.  Enable Postgres on Heroku with `$ heroku addons:create heroku-postgresql:hobby-dev` (more info and options [here](https://devcenter.heroku.com/articles/heroku-postgresql#create-a-new-database)). To initialize the production database for deployment on Heroku, open the `run` file in the projects root directory and uncomment out line 4. It should now be:

```
#!/bin/bash
set -e
python setup.py develop
initialize_db production.ini
python runapp.py
```

`$ git add run`, `$ git commit -m 'a commit message'` and then `$ git push heroku master`. This uploads the app and initializes the database. Go back to the `run` file and return it to it's previous state (line 4 should then read `# initialize_db production.ini`). This ensures that the database is not deleted and re-initialized after every push to Heroku.

## Models

`jentry_model.py` contains the `Jentry` class: the constructor for all journal entries. `journal` is a SQL table that stores all entries created using this model. `Jentry` rows contain 7 columns of data:

```python
id = Column(Integer, primary_key=True)
title = Column(Unicode)
content = Column(Unicode)  # stored as plain text/Markdown
contentr = Column(Unicode)  # content after rendering into HTML
created = Column(DateTime)  # date/time recorded at post submission
modified = Column(DateTime)  # date/time recorded after most recent edit
category = Column(Unicode)
```

## Views

Found within `routes.py` and `views/default.py`. The pages are rendered via the Jinja2 templates contained in the `templates` directory.

- All views are extensions of the base `layout.jinja2` template.
- Route `list` runs the `list_vew(request)` function. This lists all journal entries on the index of the root directory/homepage, rendered with the `list.jinja2` template.
- Route `detail` runs the `detail_view(request)` function. Accessing this route expands an individual journal entry's content in it's entirety, rendered with the `detail.jinja2` template.
- Route `create` runs the `create_view(request)` function, which is used to create a new journal entry. It is rendered with the `create.jinja2` template.
- Route `update` runs the `update_view(request)` function, which is used to edit an existing journal entry. It is rendered with the `update.jinja2` template.
- Route `delete` runs the `delete_view(request)` function, which sends you to a warning page in order to confirm the deletion of an entry. This warning page is rendered with the `delete.jinja2` template.
- Route `delete_forever` runs the `delete_forever_view(request)` function. This function permanently removes an existing journal entry from the database and sends you back to the homepage.


## Testing

### Testing Dependencies

- Pytest
- ​

Running `$ pytest --cov` runs the tests with coverage reports.