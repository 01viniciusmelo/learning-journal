# Pyramid Learning Journal Project

This repo contains the source code for my personal learning journal—created in Python using Pyramid's "alchemy" starter scaffold and Postgres. It is deployed on Heroku at http://mylearningjournal.herokuapp.com

To get started with your own version of this learning journal:
```bash
# 1. Clone this repo.
# 2. Initialize/activate your virtual environment.
# 3. Install all the required packages, including testing:
$ pip install -e . .[testing]
# 4. Erase any existing entries and initialize a new database for your local environment:
$ initialize_db development.ini
# 5. Serve the page locally.
$ pserve development.ini --reload
```

When initializing your new database, a default entry is created which you can edit or delete.

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

Running `$ pytest learning_journal --cov=learning_journal` runs the tests with coverage reports.

```
---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  10      7    30%
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/jentry_model.py       11      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/routes.py                     8      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      30     19    37%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             46      2    96%
learning_journal/views/notfound.py             4      2    50%
--------------------------------------------------------------
TOTAL                                        136     30    78%
```

### Unit Tests

- `test_new_jentry` Tests that new journal entries are added to the database.
- `test_list_view_returns_empty_when_empty` If there are no journal entries the list view should return nothing.
- `test_list_view_returns_objects_when_exist` If there are journal entries list view should return them.
- `test_detail_view_returns_dict_with_one_object` Detail view should return a dictionary.
- `test_detail_view_for_jentry_not_found` Detail view should return 404 error if nonexistent.
- `test_create_view_returns_empty_dict` Create view should return an empty dictionary.
- `test_create_view_submission_adds_new_jentry` Create view submission should add jentry to the DB.
- `test_update_view_returns_jentry` The update view's title should match the corresponding row.
- `test_update_view_submit_updates_existing_obj` Make sure the change reflects in the database.
- `test_delete_view_contains_jentry` Make sure you are deleting the right entry.

### Functional Tests

- `test_list_route_has_table` Test that the list route contains a table.
- `test_list_route_has_empty_table` Test that the table is only a header row when DB is empty.
- `test_empty_detail_route_returns_error` Test for a 404 response code on an invalid key.
- `test_list_route_has_filled_table` Test the table on list route when the databse is filled.
- `test_detail_route_returns_info` Make sure detail route prints the contents of the intialized DB.

