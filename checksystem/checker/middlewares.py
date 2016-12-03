class FirstVisitMiddleware(object):
    def process_request(self, request):
        request.first_visit = False
        if request.user.is_authenticated and request.method == 'GET' and not request.COOKIES.get('visited', False) and \
            request.user.team.contest_started():
            request.first_visit = True

    def process_response(self, request, response):
        if not hasattr(request, 'first_visit'):
            return response
        if request.method != 'GET':
            return response
        if request.first_visit:
            response.set_cookie('visited', '1')
        return response
