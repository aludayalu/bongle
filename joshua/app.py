from joshua.request import Request
from joshua.response import Http404,FileResponse,Response
from joshua.router import Router,Path

class App:
    def __init__(self):
        self.router = Router()
        self.static_dir = None
        self.static_path = None
        def set_static(self, static_path, static_dir):
            self.static_dir = static_dir
            self.static_path = static_path
        def serve_static(self, request: Request):
            new_path = request.path[len(self.static_path)::]
            return FileResponse(request, os.path.join(self.static_dir, new_path))

    def set_routes(self, routes: list):
        for path in routes:
            self.router.add_route(path)
    def __call__(self, environ, start_response):
        try:
            request = Request(environ, start_response)
            if self.static_path !=None and  request.path.startswith(self.static_path):
                response = self.serve_static(request)
                return response.make_response()
            else:
                func = self.router.get_route(request.path)
                if func is not None:
                    response: Response = func(request)
                    return response.make_response()
                else:
                    print(f'route Not found : {request.path}')
        except Exception as excplol:
            print(excplol)
        response =  Http404(request)
        return response.make_response()