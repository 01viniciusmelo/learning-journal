"""Tests for the Learning Journal application."""
# -*- coding: utf-8 -*-

import pytest
from pyramid import testing

from learning_journal.models import (
    Jentry,
    User,
    get_tm_session,
    # get_engine,
    # get_session_factory,
)
from learning_journal.models.meta import Base

import faker
import datetime
import random
import os
import transaction

from passlib.apps import custom_app_context as pwd_context


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


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    Sets up a pointer to the location of the
        database, including models.

    Tears everything down, including the in-memory database.
    """
    settings = {
        'sqlalchemy.url': 'postgres:///test_learning_journal'
    }
    config = testing.setUp(settings=settings)
    config.include('learning_journal.models')
    config.include('learning_journal.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create test DB session.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    import pdb; pdb.set_trace()
    SessionFactory = configuration.registry['dbsession_factory']  # noqa
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Fake HTTP Request.

    Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add model instances to DB.

    Every test that includes this fixture will add new random jentrys.
    """
    dummy_request.dbsession.add_all(JENTRYS)


# ======================= UNIT TESTS ======================================== #

# def test_new_jentry_is_added(db_session):
#     """New expenses get added to the database."""
#     db_session.add_all(JENTRYS)
#     query = db_session.query(Expense).all()
#     assert len(query) == len(EXPENSES)


# ============================== FUNCTIONAL TESTS =========================== #


# ---- setup ---------------------------------------------------------------- #

@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes.

    With the alchemy scaffold we need to add to our test application the
    setting for a database to be used for the models.
    We have to then set up the database by starting a database session.
    Finally we have to create all of the necessary tables that our app
    normally uses to function.
    The scope of the fixture is function-level, so every test will get a new
    test application.
    """
    from webtest import TestApp
    from learning_journal import main

    import pdb; pdb.set_trace()

    app = main({}, **{'sqlalchemy.url': 'postgres:///test_learning_journal'})
    testapp = TestApp(app)
    session_factory = app.registry["dbsession_factory"]
    engine = session_factory().bind
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Generate model instances in the db."""
    import pdb; pdb.set_trace()
    SessionFactory = testapp.app.registry["dbsession_factory"]  # noqa
    with transaction.manager:
        dbsession = get_tm_session(
            SessionFactory,
            transaction.manager
        )

    dbsession.add_all(JENTRYS)
    dbsession.add_all(USERS)

    return dbsession


# ------------- TESTS ------------------------------------------------------- #

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
