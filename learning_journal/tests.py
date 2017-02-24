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
        email='admin@gmail.com',
        author=True,
        admin=True,
        bio='I am an admin.',
    ),
    User(
        username='author',
        password=pwd_context.hash('authorpassword'),
        firstname='bob',
        lastname='dobalina',
        email='author@gmail.com',
        author=True,
        admin=False,
        bio='I am an author.',
    ),
    User(
        username='user',
        password=pwd_context.hash('userpassword'),
        firstname='bob',
        lastname='dobalina',
        email='user@gmail.com',
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


@pytest.fixture
def db_session(configuration, request):
    """Create test DB session.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
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
    dummy_request.dbsession.add_all(USERS)


def test_new_jentry_is_added(
        db_session):
    """New journal entry should be added to the database."""
    db_session.add_all(JENTRYS)
    query = db_session.query(Jentry).all()
    assert len(query) == len(JENTRYS)


def test_home_view_returns_empty_when_empty(
        dummy_request):
    """Test that the list view returns no objects when none added."""
    from .views.default import home_view
    result = home_view(dummy_request)
    assert len(result["journal"]) == 0


def test_home_view_returns_objects_when_exist(
        dummy_request, add_models):
    """Test that the list view does return objects when the DB is populated."""
    from .views.default import home_view
    result = home_view(dummy_request)
    assert len(result["journal"]) == 100


def test_detail_view_contains_individual_expense_details(
        db_session, dummy_request, add_models):
    """Test that the detail view actually returns individual entry info."""
    from .views.default import detail_view
    dummy_request.matchdict["id"] = 12
    jentry = db_session.query(Jentry).get(12)
    result = detail_view(dummy_request)
    assert result["jentry"] == jentry


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
    SessionFactory = testapp.app.registry["dbsession_factory"]  # noqa
    with transaction.manager:
        dbsession = get_tm_session(
            SessionFactory,
            transaction.manager
        )

    dbsession.add_all(JENTRYS)
    dbsession.add_all(USERS)

    return dbsession


def test_home_page_pops_up(testapp):
    """Test that home page get sent correctly."""
    response = testapp.get('/')
    assert response.status_code == 200


def test_login_view_ok(testapp):
    """Test login view."""
    response = testapp.get('/login')
    assert response.status_code == 200


def test_logout_view_redirects(testapp):
    """Logout view should redirect."""
    response = testapp.get('/logout')
    assert response.status_code == 302


def test_register_view_ok(testapp):
    """Register view should be ok."""
    response = testapp.get('/register')
    assert response.status_code == 200


def test_register_new_user(testapp):
    """Registration page should create a new user in the database."""
    user = {
        'username': 'bobbydobalina',
        'password': 'password',
        'firstname': 'bob',
        'lastname': 'dobalina',
        'email': 'email@address.com',
        'bio': 'bio',

    }
    html = testapp.post('/register', user, status=302).follow().html
    assert 'email@address.com' in html.find_all('li')[2].text
    assert 'bob dobalina' in html.find_all('li')[1].text


def test_successful_login_leads_somewhere(testapp, fill_the_db):
    """Test that after logging in it sends you somewhere."""
    response = testapp.post(
        '/login',
        params={
            'username': 'admin',
            'password': 'password'}
    )
    assert response.status_code == 200


def test_successful_login_shows_table(testapp, fill_the_db):
    """Test that after logging in you see a table of data."""
    response = testapp.get('/login')
    assert response.status_code == 200
    assert response.html.find('form')


def test_logout(testapp, fill_the_db):
    """Test that after logging out a login link exists."""
    testapp.post('/login',
                 params={'username': 'admin',
                         'password': 'password'})
    response = testapp.get('/logout', status=302).follow()
    assert response.status_code == 200
    assert response.html.find_all('a')[1].text == ' Login '
