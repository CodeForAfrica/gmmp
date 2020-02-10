from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from jet.dashboard.modules import DashboardModule

from forms.models import (
    InternetNewsSheet,
    NewspaperSheet,
    RadioSheet,
    TelevisionSheet,
    TwitterSheet,
)


class AddInternetNewsSubmission(DashboardModule):
    title = _("Add Internet News Submissions")
    url = reverse("admin:forms_internetnewssheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Internet News Submissions"),
                "url": reverse("admin:forms_internetnewssheet_add"),
            },
        ]


class AddNewspaperSubmission(DashboardModule):
    title = _("Add Newspaper Submissions")
    url = reverse("admin:forms_newspapersheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Newspaper Submissions"),
                "url": reverse("admin:forms_newspapersheet_add"),
            },
        ]


class AddRadioSubmission(DashboardModule):
    title = _("Add Radio Submissions")
    url = reverse("admin:forms_radiosheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Radio Submissions"),
                "url": reverse("admin:forms_radiosheet_add"),
            },
        ]


class AddTelevisionSubmission(DashboardModule):
    title = _("Add Television Submissions")
    url = reverse("admin:forms_televisionsheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Television Submissions"),
                "url": reverse("admin:forms_televisionsheet_add"),
            },
        ]


class AddTwitterSubmission(DashboardModule):
    title = _("Add Twitter Submissions")
    url = reverse("admin:forms_twittersheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Twitter Submissions"),
                "url": reverse("admin:forms_twittersheet_add"),
            },
        ]


class Submissions(DashboardModule):
    title = "Submissions"
    template = "gmmp/dashboard_modules/submissions.html"

    def init_with_context(self, context):
        self.children = [
            {
                "name": _("Newspaper Submission(s)"),
                "count": NewspaperSheet.objects.count(),
                "url": reverse("admin:forms_newspapersheet_changelist"),
            },
            {
                "name": _("Radio Submission(s)"),
                "count": RadioSheet.objects.count(),
                "url": reverse("admin:forms_radiosheet_changelist"),
            },
            {
                "name": _("Television Submission(s)"),
                "count": TelevisionSheet.objects.count(),
                "url": reverse("admin:forms_televisionsheet_changelist"),
            },
            {
                "name": _("Internet News Submission(s)"),
                "count": InternetNewsSheet.objects.count(),
                "url": reverse("admin:forms_internetnewssheet_changelist"),
            },
            {
                "name": _("Twitter Submission(s)"),
                "count": TwitterSheet.objects.count(),
                "url": reverse("admin:forms_twittersheet_changelist"),
            },
        ]
