"""Tests for the Learning Journal application."""
# -*- coding: utf-8 -*-

import pytest
from pyramid import testing

from learning_journal.models import Jentry, get_tm_session
from learning_journal.models.meta import Base

import faker
import datetime
import random
import os
import transaction


# =============== TEST JENTRYS ================

FAKE = faker.Faker()
now = datetime.datetime.now()
CATEGORIES = [
    "history",
    "economics",
    "current events",
    "distractions",
    "python",
    "music production",
    "new music",
    "environment",
    "cool ideas",
    "the end of the world",
]

JENTRYS = [
    Jentry(
        title=FAKE.job(),
        content=FAKE.text(max_nb_chars=200),
        contentr='',
        created=now,
        modified=now,
        category=random.choice(CATEGORIES)
    ) for i in range(100)
]


# ================== UNIT TESTS SESSION =====================


@pytest.fixture(scope="session")
def configuration(request):
    """Configurator."""
    config = testing.setUp(settings={'sqlalchemy.url': 'sqlite:///:memory:'})
    config.include('learning_journal.models')
    config.include('learning_journal.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def db_session(configuration, request):
    """Create test DB session."""
    SessionFactory = configuration.registry['dbsession_factory']  # noqa
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Make a fake HTTP request with DB Session."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Generate model instances in the db."""
    dummy_request.dbsession.add_all(JENTRYS)


# ============ UNIT TESTS ===============

def test_new_jentry(db_session):
    """New journals are added to the database."""
    db_session.add_all(JENTRYS)
    query = db_session.query(Jentry).all()
    assert len(query) == len(JENTRYS)


def test_list_view_returns_empty_when_empty(dummy_request):
    """Test that the list view returns nothing."""
    from learning_journal.views.default import list_view
    result = list_view(dummy_request)
    assert len(result["journal"]) == 0


def test_list_view_returns_objects_when_exist(dummy_request, add_models):
    """Test that list view returns objects when they exist in the DB."""
    from learning_journal.views.default import list_view
    result = list_view(dummy_request)
    assert len(result["journal"]) == 100


def test_detail_view_returns_dict_with_one_object(dummy_request, add_models):
    """Detail view should return a dict."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict["id"] = "4"
    result = detail_view(dummy_request)
    jentry = dummy_request.dbsession.query(Jentry).get(4)
    assert result["jentry"] == jentry


def test_detail_view_for_jentry_not_found(dummy_request):
    """Nonexistent jentrys return 404 error."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict["id"] = "2103944"
    result = detail_view(dummy_request)
    assert result.status_code == 404


def test_create_view_returns_empty_dict(dummy_request):
    """Get create view should return an empty dict."""
    from learning_journal.views.default import create_view
    assert create_view(dummy_request) == {}


def test_create_view_submission_adds_new_jentry(dummy_request):
    """Submitting the new entry form creates a new jentry in the db."""
    from learning_journal.views.default import create_view

    query = dummy_request.dbsession.query(Jentry)
    count = query.count()

    dummy_request.method = "POST"
    dummy_request.POST["title"] = "test title"
    dummy_request.POST["content"] = "## Test content."
    dummy_request.POST["contentr"] = "<h2>Test content.</h2>"
    dummy_request.POST["created"] = now
    dummy_request.POST["lastmodified"] = now
    dummy_request.POST["category"] = 'Empty Category'
    create_view(dummy_request)

    new_count = query.count()
    assert new_count == count + 1


def test_update_view_returns_returns_jentry(dummy_request, add_models):
    """Update view should return the jentry data."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict["id"] = "4"
    result = update_view(dummy_request)
    jentry = dummy_request.dbsession.query(Jentry).get(4)
    assert result["jentry"].title == jentry.title


def test_update_view_submit_updates_exisiting_obj(dummy_request, add_models):
    """Submitting in the edit view should update the object."""
    from learning_journal.views.default import update_view

    query = dummy_request.dbsession.query(Jentry)

    dummy_request.method = "POST"
    dummy_request.matchdict["id"] = "4"
    dummy_request.POST["title"] = "test title"
    dummy_request.POST["content"] = "## Test content."
    dummy_request.POST["contentr"] = "<h2>Test content.</h2>"
    dummy_request.POST["created"] = now
    dummy_request.POST["lastmodified"] = now
    dummy_request.POST["category"] = 'Empty Category'
    update_view(dummy_request)

    jentry = query.get(4)
    assert jentry.title == "test title"


# =========== FUNCTIONAL TESTS SESSION ==============

@pytest.fixture(scope="session")
def testapp(request):
    """Test routes."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main(global_config, **settings):
        """Return a pyramid WSGI application."""
        settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({}, **{})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]  # noqa
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tear_down():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tear_down)
    return testapp


@pytest.fixture
def fill_db(testapp):
    """Fill database with Jentrys."""
    SessionFactory = testapp.app.registry["dbsession_factory"]  # noqa
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(JENTRYS)

        return dbsession


# ============== FUNCTIONAL TESTS ================

def test_list_route_has_table(testapp):
    """The index contains an html table."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("table")) == 1


def test_list_route_has_empty_table(testapp):
    """The table should only have a header row."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("tr")) == 1
