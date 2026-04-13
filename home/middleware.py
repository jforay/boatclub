from django.http import HttpResponsePermanentRedirect

class RedirectCarolinasMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().lower()
        if 'carolinas' in host:
            return HttpResponsePermanentRedirect('https://www.destinationboatclub.com' + request.path)
        return self.get_response(request)