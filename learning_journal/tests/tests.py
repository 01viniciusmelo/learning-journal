"""Tests for the Learning Journal application."""
# -*- coding: utf-8 -*-


import pytest
from pyramid import testing

from learning_journal.models import Jentry, get_tm_session
from learning_journal.models.meta import Base


@pytest.fixture(scope="session")
def configuration(request):
    """Configurator."""
    config = testing.setUp(settings={'sqlalchemy.url': 'sqlite:///:memory:'})
    config.include('.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def make_session(configuration, request):
    """Create new database session for testing."""
    session_factory = configuration.registry['dbsession_factory']
    session = session_factory()
    engine = session.bind
    Jentry.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session
