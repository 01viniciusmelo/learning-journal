"""Routes."""
# -*- coding: utf-8 -*-


def includeme(config):
    """Include me."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    # ------- PUBLIC
    config.add_route('list', '/')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('profile', '/profile/{id:\d+}')
    # ------- GET PERMISSION
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    # ------- AUTHOR VIEWS
    config.add_route('create', '/journal/new-entry')
    config.add_route('update', '/journal/{id:\d+}/edit-entry')
    config.add_route('delete', '/journal/{id:\d+}/delete-entry')
    config.add_route('delete_forever', '/journal/{id:\d+}/delete-forever')
