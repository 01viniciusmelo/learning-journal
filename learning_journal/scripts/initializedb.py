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

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models import Jentry


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
    settings = get_appsettings(config_uri, options=options)  # Access database
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]
    engine = get_engine(settings)  # Start interaction

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        now = datetime.datetime.now()
        jentry_model = Jentry(
            title='First Entry',
            content='## This is the entries content.',
            contentr='<h2>This is the entries content.</h2>',
            created=now,
            modified=now,
            category='Empty Category'
        )
        dbsession.add(jentry_model)
