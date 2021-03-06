"""Initialize database."""


import os
import sys
import transaction
import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars

from learning_journal.models.meta import Base
from learning_journal.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    Jentry,
    User,
)


def usage(argv):
    """Usage."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Main function."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        now = datetime.datetime.now()
        jentry_init = Jentry(
            title='Test Entry',
            author_username='admin',
            content='## This is the entries content.',
            contentr='<h2>This is the entries content.</h2>',
            created=now,
            modified=now,
            category='Empty Category',
        )
        dbsession.add(jentry_init)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        admin = User(
            username="admin",
            password="password",
            firstname="Admin",
            lastname="Admin",
            email="admin@email.com",
            author=True,
            admin=True,
            bio=""
        )
        benny = User(
            username="benny",
            password="password",
            firstname="Ben",
            lastname="Petty",
            email="benjamin.s.petty@gmail.com",
            author=True,
            admin=True,
            bio="",
        )
        dbsession.add(admin)
        dbsession.add(benny)
