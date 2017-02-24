"""Routes."""
# -*- coding: utf-8 -*-


def includeme(config):
    """Include me."""
    config.add_static_view(
        'static', 'learning_journal:static', cache_max_age=3600)
    # ------- PUBLIC ----------------------------------------------------------
    config.add_route('home', '/')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('profile', '/profile/{username:[\d\w]+}')
    # ------- GET PERMISSION --------------------------------------------------
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    # config.add_route('register', '/register')
    # ------- USER VIEWS ------------------------------------------------------
    config.add_route('delete_user', '/delete_user/{username:[\d\w]+}')
    # ------- AUTHOR VIEWS ----------------------------------------------------
    config.add_route('create', '/journal/new-entry')
    config.add_route('update', '/journal/{id:\d+}/edit-entry')
    config.add_route('delete', '/journal/{id:\d+}/delete-entry')
    config.add_route('delete_forever', '/journal/{id:\d+}/delete-forever')
    # ------- ADMIN VIEWS -----------------------------------------------------
    config.add_route('users', '/users')
    config.add_route('admin_register', '/admin_register')
    config.add_route('delete_user_forever',
                     '/delete_user_forever/{username:[\d\w]+}')
