"""Tests for the Learning Journal application."""

import pytest
from pyramid import testing


@pytest.fixture(scope="session")
def configuration(request):
    """Configurator instance.

    Sets up a pointer to the database,
    includes all models,
    then tears everything down!

    Configuration applies while Pytest is running.
    """
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:'
    }

    config = testing.setUp(settings=settings)
    config.include('.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config
