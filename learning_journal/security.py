"""Security."""

import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory


from passlib.apps import custom_app_context as pwd_context

from learning_journal.models import User


class MyRoot(object):
    """Root object."""

    def __init__(self, request):
        """Root init."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'admin'),
    ]


def check_credentials(request):
    """Check user credentials."""
    if "username" in request.POST and "password" in request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        query = request.dbsession.query(User)
        user_logging_in = query.filter(User.username == username).first()
        if user_logging_in:
            return pwd_context.verify(password, user_logging_in.password)
    return False


def includeme(config):
    """Security-related configuration."""
    auth_secret = os.environ.get('AUTH_SECRET', 'potato')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(MyRoot)
    session_secret = os.environ.get("SESSION_SECRET", "potatos")
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
