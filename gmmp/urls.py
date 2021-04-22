import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView, TemplateView

from gmmp import settings
from gmmp.views import CustomPassowrdResetView, CustomPasswordResetDoneView

admin.site.site_header = settings.ADMIN_SITE_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_SITE_TITLE
admin.site.site_url = settings.ADMIN_SITE_SITE_URL
admin.site.index_title = settings.ADMIN_SITE_INDEX_TITLE

urlpatterns = (
    i18n_patterns(
        # Django JET URLS
        re_path(r"^jet/", include("jet.urls", "jet")),
        # Django JET dashboard URLS
        re_path(r"^jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
        path(
            "admin/password_reset/",
            CustomPassowrdResetView.as_view(),
            name="admin_password_reset",
        ),
        path(
            "admin/password_reset/done/",
            CustomPasswordResetDoneView.as_view(),
            name="password_reset_done",
        ),
        path(
            "reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(),
            name="password_reset_confirm",
        ),
        path(
            "reset/done/",
            auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete",
        ),
        # Admin site URLS
        path("admin/", admin.site.urls),
        re_path(r"^$", RedirectView.as_view(url="/admin"), name="go-to-admin"),
        path('reports/', include('reports.urls')),
        prefix_default_language=False,
    )
    + [path('__debug__/', include(debug_toolbar.urls))]
    + [path("", include("gsheets.urls"))]
    + [path("i18n/", include("django.conf.urls.i18n"))]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
