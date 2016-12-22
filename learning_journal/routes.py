"""Routes."""


def includeme(config):
    """Include me."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('detail', '/detail')
    config.add_route('create', '/new-model')
    config.add_route('update', '/update')
