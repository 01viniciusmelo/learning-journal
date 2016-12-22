"""Default."""


from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Entry


@view_config(route_name='index', renderer='../templates/index.jinja2')
def my_view(request):
    """My view."""
    try:
        query = request.dbsession.query(Entry)
        one = query.filter(Entry.id == '1').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'learning-journal'}


@view_config(route_name="detail",
             renderer="../templates/detail.jinja2")
def detail_view(request):
    """Create view."""
    if request.method == "POST":
        # get the form stuff
        return {}
    return {}


@view_config(route_name="create",
             renderer="../templates/create.jinja2")
def create_view(request):
    """Create view."""
    if request.method == "POST":
        # get the form stuff
        return {}
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning-journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
