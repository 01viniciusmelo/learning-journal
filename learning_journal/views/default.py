"""Default views."""
# -*- coding: utf-8 -*-


import datetime
import markdown
from jinja2 import Markup

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from sqlalchemy.exc import DBAPIError

from learning_journal.models import Jentry, User
from learning_journal.security import check_credentials


# ============================= PUBLIC VIEWS ================================ #

@view_config(
    route_name="list",
    renderer="../templates/list.jinja2",
)
def list_view(request):
    """Homepage view lists all existing journal entries."""
    try:
        query = request.dbsession.query(Jentry).order_by(Jentry.id.desc())
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'journal': query.all(), 'project': 'learning_journal'}


@view_config(
    route_name="detail",
    renderer="../templates/detail.jinja2",
)
def detail_view(request):
    """Detail view expands an individual entry."""
    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    if not jentry:
        return Response("Not Found", content_type='text/plain', status=404)
    jentry.contentr = Markup(markdown.markdown(jentry.content, [
        'markdown.extensions.nl2br',
        'markdown.extensions.codehilite',
        'markdown.extensions.smarty',
        'fenced_code', ]))
    return {"jentry": jentry}


@view_config(
    route_name="profile",
    renderer="../templates/profile.jinja2",
)
def profile_view(request):
    """Profile view displays a users profile info."""
    user_id = int(request.matchdict["id"])
    user = request.dbsession.query(User).get(user_id)
    if not user:
        return Response("Not Found", content_type='text/plain', status=404)
    return {"user": user}


# ===================== GET PERMISSION VIEWS ================================ #

@view_config(
    route_name="login",
    renderer="../templates/login.jinja2",
)
def login_view(request):
    """Login view."""
    if request.method == "POST" and request.POST:
        if check_credentials(request):
            auth_head = remember(request, request.POST["username"])
            return HTTPFound(request.route_url("list"), headers=auth_head)
    return {}


@view_config(
    route_name="logout",
)
def logout_view(request):
    """Logout view."""
    empty_head = forget(request)
    return HTTPFound(request.route_url('list'), headers=empty_head)


@view_config(
    route_name="register",
    renderer="../templates/register.jinja2",
)
def register_view(request):
    """Registration view."""
    if request.method == "POST" and request.POST:
        new_user = User(
            username=request.POST["username"],
            password=request.POST["password"],
            firstname=request.POST["firstname"],
            lastname=request.POST["lastname"],
            email=request.POST["email"],
        )
        request.dbsession.add(new_user)
        return HTTPFound(request.route_url("list"))
    return {}


# =============================== AUTHOR VIEWS ============================== #

@view_config(
    route_name="create",
    renderer="../templates/create.jinja2",
    permission="author",
)
def create_view(request):
    """Create view makes a new post."""
    if request.method == "POST":
        title = request.POST['title']
        category = request.POST['category']
        content = request.POST['content']
        now = datetime.datetime.now()
        jentry = Jentry(
            title=title,
            category=category,
            created=now,
            modified=now,
            content=content
        )
        request.dbsession.add(jentry)
        return HTTPFound(request.route_url('list'))
    return {}


@view_config(
    route_name="update",
    renderer="../templates/update.jinja2",
    permission="author",
)
def update_view(request):
    """Update view edits an existing entry."""
    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    if request.method == "POST":
        jentry.title = request.POST['title']
        jentry.category = request.POST['category']
        jentry.content = request.POST['content']
        jentry.modified = datetime.datetime.now()
        return HTTPFound(request.route_url('detail', id=jentry_id))
    return {"jentry": jentry}


@view_config(
    route_name="delete",
    renderer="../templates/delete.jinja2",
    permission="author",
)
def delete_view(request):
    """Delete view shows a warning pre confirmation of an entry deletion."""
    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    return {"jentry": jentry}


# TODO:
# @view_config(route_name="delete_forever")
# def delete_forever_view(request):
#     """Delete forever permanently removes an entry from the database."""
#     return


# =========================================================================== #

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
