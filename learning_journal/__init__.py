"""Initializes the Learning Journal."""

from pyramid.config import Configurator
import os


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]
    # TODO:  ^^
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()
