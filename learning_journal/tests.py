"""Tests for the Learning Journal application."""
# -*- coding: utf-8 -*-

import pytest
from pyramid import testing

from learning_journal.models import (
    Jentry,
    User,
    get_tm_session,
    get_engine,
    get_session_factory,
)
from learning_journal.models.meta import Base

import faker
import datetime
import random
import os
import transaction

from passlib.apps import custom_app_context as pwd_context


# ================================ TEST MODELS ============================= #


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
        author_username=FAKE.first_name(),
        created=now,
        modified=now,
        category=random.choice(CATEGORIES),
    ) for i in range(100)
]

USERS = [
    User(
        username='admin',
        password=pwd_context.hash('password'),
        firstname='bob',
        lastname='dobalina',
        email='admin@imager.com',
        author=True,
        admin=True,
        bio='I am an admin.',
    ),
    User(
        username='author',
        password=pwd_context.hash('authorpassword'),
        firstname='bob',
        lastname='dobalina',
        email='author@imager.com',
        author=True,
        admin=False,
        bio='I am an author.',
    ),
    User(
        username='user',
        password=pwd_context.hash('userpassword'),
        firstname='bob',
        lastname='dobalina',
        email='user@imager.com',
        author=False,
        admin=False,
        bio='I am but a meer user.',
    ),
]


# =========================== FIXTURES ====================================== #


@pytest.fixture(scope="session")
def sqlengine(request):
    """Configurator."""
    settings = {'sqlalchemy.url': os.environ["DATABASE_URL"]}
    config = testing.setUp(settings=settings)
    config.include('learning_journal.models')
    config.include('learning_journal.routes')
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def db_session(sqlengine, request):
    """Create test DB session."""
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session, method="GET"):
    """Make a fake HTTP GET request with DB Session."""
    request = testing.DummyRequest
    request.method = method
    request.dbsession = db_session
    return request


@pytest.fixture
def dummy_post_request(db_session, method="POST"):
    """Make a fake HTTP POST request with a DB Session."""
    request = testing.DummyRequest()
    request.method = method
    request.dbsession = db_session
    return request


@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes."""
    from webtest import TestApp
    from learning_journal import main

    app = main({}, **{'sqlalchemy.url': os.environ["DATABASE_URL"]})
    testapp = TestApp(app)
    session_factory = app.registry["dbsession_factory"]
    engine = session_factory().bind
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Generate model instances in the db."""
    SessionFactory = testapp.app.registry["dbsession_factory"]  # noqa
    with transaction.manager:
        dbsession = get_tm_session(
            SessionFactory,
            transaction.manager
        )

    dbsession.add_all(JENTRYS)
    dbsession.add_all(USERS)

    return dbsession


# ============================== FUNCTIONAL TESTS =========================== #


def test_home_page_pops_up(testapp):
    """Test that home page get sent correctly."""
    response = testapp.get('/', status=200)
    assert response.status_code == 200


def test_successful_login_leads_somewhere(testapp, fill_the_db):
    """Test that after logging in it sends you somewhere."""
    response = testapp.post(
        '/login',
        params={
            'username': 'admin',
            'password': 'password'}
    )
    assert response.status_code == 200
