
class Path:
#this class holds our directory listingz
    __slots__ = 'path', 'func'

    def __init__(self, _path: str, _func):
        self.path = _path
        self.func = _func

    def match(self, _path):
        # function to check if the url matches on of the listed directories of our wsgi
        # Extractin vars like django
        if self.path == _path:
            return True
        return False

class Router:
#the class holds the sub directory listings and checks it on incoming requests
    __slots__ = 'routes'

    def __init__(self, routes: list = None):
        self.routes: list = list(routes) if routes else []

    def add_route(self, _path: Path):
        self.routes.append(_path)
        return True

    def get_route(self, path_):
        for path in self.routes:
            if path.match(path_):
                return path.func