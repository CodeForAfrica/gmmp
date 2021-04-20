from django.shortcuts import redirect
from whitenoise.middleware import WhiteNoiseMiddleware


class ProtectedStaticFileMiddleware(WhiteNoiseMiddleware):
    def process_request(self, request):
        # check user authentication
        if request.path != '/static/wazimap/index.html' or request.user.is_authenticated:
            return WhiteNoiseMiddleware().process_request(request)
        return redirect('/admin/login/?next=/static/wazimap/index.html')
