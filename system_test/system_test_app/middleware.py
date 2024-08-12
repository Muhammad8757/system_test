class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        path = request.path

        check_paths = {
            '/api/v1/theme/',
            '/api/v1/test/',
            '/api/v1/activate/',
        }
        
        if path in check_paths:
            if not hasattr(request.user, 'is_teacher') or not request.user.is_teacher:
                raise Exception("you do not have permission to perform this action.")
        response = self.get_response(request)
        return response