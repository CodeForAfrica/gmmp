from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gmmp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^$', TemplateView.as_view(template_name="index.html")),
)

