"""Default."""

import datetime

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from ..models import Jentry


@view_config(route_name='list',
             renderer='../templates/list.jinja2')
def list_view(request):
    """My view."""
    try:
        query = request.dbsession.query(Jentry).order_by(Jentry.id.desc())
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'journal': query.all(), 'project': 'learning-journal'}


@view_config(route_name="detail",
             renderer="../templates/detail.jinja2")
def detail_view(request):
    """Create view."""
    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    return {"jentry": jentry}


@view_config(route_name="create",
             renderer="../templates/create.jinja2")
def create_view(request):
    """Create view."""
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        now = datetime.datetime.now()
        jentry = Jentry(title=title,
                        created=now,
                        modified=now,
                        content=content
                        )
        request.dbsession.add(jentry)
        return HTTPFound(request.route_url('list'))
    return {}


@view_config(route_name="update",
             renderer="../templates/update.jinja2")
def update_view(request):
    """Update view."""
    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    if request.method == "POST":
        jentry.title = request.POST['title']
        jentry.content = request.POST['content']
        jentry.modified = datetime.datetime.now()
        return HTTPFound(request.route_url('list'))
    return {"jentry": jentry}


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
