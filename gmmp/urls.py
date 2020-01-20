from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'gmmp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    re_path(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    re_path(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls), # admin site
    
    re_path(r'^$', TemplateView.as_view(template_name="index.html")),

    # TODO: Fix reports views, they're blocking migration
    # url(r'^reports/', include('reports.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
