"""Default views."""
# -*- coding: utf-8 -*-


import datetime
import markdown
from jinja2 import Markup

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import remember, forget
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from learning_journal.models import Jentry, User
from learning_journal.security import check_credentials

from passlib.apps import custom_app_context as pwd_context


# ============================= PUBLIC VIEWS ================================ #

@view_config(
    route_name="home",
    renderer="../templates/home.jinja2",
)
def home_view(request):
    """List all existing journal entries on the home page."""
    try:
        journal = request.dbsession.query(Jentry).order_by(Jentry.id.desc())
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    return {
        'journal': journal.all(),
        'user': user,
    }


@view_config(
    route_name="detail",
    renderer="../templates/detail.jinja2",
)
def detail_view(request):
    """Expand an individual entry."""
    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    if not jentry:
        return Response("Not Found", content_type='text/plain', status=404)
    author = request.dbsession.query(
        User).filter_by(username=jentry.author_username).first()
    jentry.contentr = Markup(markdown.markdown(jentry.content, [
        'markdown.extensions.nl2br',
        'markdown.extensions.codehilite',
        'markdown.extensions.smarty',
        'fenced_code', ]))

    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    return {
        "jentry": jentry,
        "user": user,
        "author": author,
    }


@view_config(
    route_name="profile",
    renderer="../templates/profile.jinja2",
)
def profile_view(request):
    """View or edit your user profile."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------
    username = request.matchdict["username"]
    profile = request.dbsession.query(
        User).filter_by(username=username).first()
    if not profile:
        return Response("Not Found", content_type='text/plain', status=404)
    if request.method == 'POST' and request.POST:
        if 'author' in request.POST:
            profile.author = not bool(profile.author)
            return HTTPFound(
                request.route_url('profile', username=profile.username))
        else:
            if request.POST["password"] != '':
                profile.password = pwd_context.hash(request.POST["password"])
            profile.firstname = request.POST["firstname"]
            profile.lastname = request.POST["lastname"]
            profile.email = request.POST["email"]
            profile.bio = request.POST["bio"]
            return HTTPFound(
                request.route_url('profile', username=profile.username))
    return {
        "profile": profile,
        "user": user
    }


# ===================== GET PERMISSION VIEWS ================================ #


@view_config(
    route_name="login",
    renderer="../templates/login.jinja2",
)
def login_view(request):
    """Login view."""
    if request.method == "POST" and request.POST:
        if check_credentials(request):
            auth_head = remember(
                request,
                request.POST["username"]
            )
            return HTTPFound(
                request.route_url('home'),
                headers=auth_head,
            )
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
        return HTTPFound(
            request.route_url('home'),
            headers=auth_head,
        )
    else:
        user = None
    # ------------
    return {"user": user}


# ...


@view_config(
    route_name="logout",
)
def logout_view(request):
    """Logout view."""
    empty_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=empty_head)


# ...


# @view_config(
#     route_name="register",
#     renderer="../templates/register.jinja2",
# )
# def register_view(request):
#     """Registration view."""
#     if request.method == "POST" and request.POST:
#         if request.POST["username"] and len(
#                 request.POST["username"].split()) > 1:
#             new_name = request.POST["username"].split()
#             new_name = str.lower('_'.join(new_name))
#         else:
#             new_name = request.POST["username"]
#             new_name = str.lower(str(new_name))
#         new_user = User(
#             username=new_name,
#             password=pwd_context.hash(request.POST["password"]),
#             firstname=request.POST["firstname"],
#             lastname=request.POST["lastname"],
#             email=request.POST["email"],
#             bio=request.POST["bio"],
#             author=False,
#             admin=False,
#         )
#         request.dbsession.add(new_user)
#         auth_head = remember(request, new_name)
#         return HTTPFound(request.route_url(
#             'profile', username=new_name),
#             headers=auth_head)
#     # --- user ---
#     if request.authenticated_userid:
#         user = request.dbsession.query(User).filter_by(
#             username=request.authenticated_userid).first()
#     else:
#         user = None
#     # ------------
#     return {"user": user}


# ================ USER VIEWS =================================================


@view_config(
    route_name="delete_user",
    renderer="../templates/delete_user.jinja2",
    permission="view",
    require_csrf=True,
)
def delete_user_view(request):
    """Delete user shows a warning pre confirmation of a user deletion."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    delete_username = request.matchdict["username"]
    user_to_delete = request.dbsession.query(
        User).filter_by(username=delete_username).first()
    try:
        if user.admin or user == user_to_delete:
            return {
                "delete_user": user_to_delete,
                "user": user,
            }
        else:
            return HTTPForbidden
    except AttributeError:
        return HTTPForbidden


# =============================== AUTHOR VIEWS ============================== #


@view_config(
    route_name="create",
    renderer="../templates/create.jinja2",
    permission="admin",
    require_csrf=True,
)
def create_view(request):
    """Create view makes a new post."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    if request.method == "POST":
        now = datetime.datetime.now()
        jentry = Jentry(
            title=request.POST['title'],
            category=request.POST['category'],
            author_username=user.username,
            created=now,
            modified=now,
            content=request.POST['content']
        )
        request.dbsession.add(jentry)
        return HTTPFound(request.route_url('home'))
    try:
        journal = request.dbsession.query(
            Jentry).order_by(
                Jentry.id.desc()
        )
    except DBAPIError:
        return Response(
            db_err_msg,
            content_type='text/plain',
            status=500
        )
    return {
        "user": user,
        "journal": journal.all()
    }


@view_config(
    route_name="update",
    renderer="../templates/update.jinja2",
    permission="admin",
    require_csrf=True,
)
def update_view(request):
    """Update view edits an existing entry."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    if request.method == "POST":
        jentry.title = request.POST['title']
        jentry.category = request.POST['category']
        jentry.content = request.POST['content']
        jentry.modified = datetime.datetime.now()
        return HTTPFound(request.route_url('detail', id=jentry_id))
    return {
        "jentry": jentry,
        "user": user
    }


@view_config(
    route_name="delete",
    renderer="../templates/delete.jinja2",
    permission="admin",
    require_csrf=True,
)
def delete_view(request):
    """Delete view shows a warning pre confirmation of an entry deletion."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    return {
        "jentry": jentry,
        "user": user
    }


@view_config(
    route_name="delete_forever",
    permission="admin",
    require_csrf=True,
)
def delete_forever_view(request):
    """Delete forever permanently removes an entry from the database."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    jentry_id = int(request.matchdict["id"])
    jentry = request.dbsession.query(Jentry).get(jentry_id)
    if user.username == jentry.author_username:
        request.dbsession.delete(jentry)
        return HTTPFound(request.route_url('home'))
    else:
        return HTTPForbidden
    return {"user": user}


# ============================== ADMIN VIEWS ================================ #


@view_config(
    route_name="users",
    renderer="../templates/users.jinja2",
    permission="admin",
    require_csrf=True,
)
def users_view(request):
    """Add/edit/delete users and grant permissions."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------

    users = request.dbsession.query(User).order_by(User.username.asc())

    return {
        "user": user,
        "users": users,
    }


@view_config(
    route_name="admin_register",
    renderer="../templates/register.jinja2",
    permission="admin",
    require_csrf=True,
)
def admin_register_view(request):
    """Registration view."""
    if request.method == "POST" and request.POST:
        if request.POST["username"] and len(
                request.POST["username"].split()) > 1:
            new_name = request.POST["username"].split()
            new_name = str.lower('_'.join(new_name))
        else:
            new_name = request.POST["username"]
            new_name = str.lower(str(new_name))
        new_user = User(
            username=new_name,
            password=pwd_context.hash(request.POST["password"]),
            firstname=request.POST["firstname"],
            lastname=request.POST["lastname"],
            email=request.POST["email"],
            bio=request.POST["bio"],
            author=False,
            admin=False,
        )
        request.dbsession.add(new_user)
        return HTTPFound(
            request.route_url('profile', username=new_name),
        )
    user = None
    return {"user": user}


@view_config(
    route_name='delete_user_forever',
    permission="admin",
    require_csrf=True,
)
def delete_user_forever_view(request):
    """Delete user from the DB."""
    # --- user ---
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    # ------------
    delete_username = request.matchdict["username"]
    user_to_delete = request.dbsession.query(
        User).filter_by(username=delete_username).first()
    if not user_to_delete.admin:
        request.dbsession.delete(user_to_delete)
    if user.admin:
        return HTTPFound(request.route_url('users'))
    elif user_to_delete.username == request.authenticated_userid:
        empty_head = forget(request)
        return HTTPFound(request.route_url('home'), headers=empty_head)


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
