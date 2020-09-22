from django.contrib.auth import views as auth_views
from gmmp import settings


class CustomPassowrdResetView(auth_views.PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_header'] = settings.ADMIN_SITE_SITE_HEADER
        return context

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_header'] = settings.ADMIN_SITE_SITE_HEADER
        return context
