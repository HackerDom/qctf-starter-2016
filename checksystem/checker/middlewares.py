class FirstVisitMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.first_visit = False
            if not request.COOKIES.get('visited', False):
                request.first_visit = True

    def process_response(self, request, response):
        if not request.user.is_authenticated or request.method == 'POST':
            return response
        if not request.COOKIES.get('visited', False):
            response.set_cookie('visited', '1')
        return response
