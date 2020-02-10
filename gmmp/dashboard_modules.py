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
    title = _("Internet News")
    url = reverse("admin:forms_internetnewssheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Internet News Article"),
                "url": reverse("admin:forms_internetnewssheet_add"),
                "description": _(
                    "Capture here news that are online. Remember to only capture national (and if necessary, local) major websites."
                ),
            },
        ]


class AddNewspaperSubmission(DashboardModule):
    title = _("Newspapers")
    url = reverse("admin:forms_newspapersheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Newspaper Article"),
                "url": reverse("admin:forms_newspapersheet_add"),
                "description": _(
                    "Newspaper news are news published on print. The number of newspapers you code will depend on the number of newspapers in your country."
                ),
            },
        ]


class AddRadioSubmission(DashboardModule):
    title = _("Radio News")
    url = reverse("admin:forms_radiosheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Radio Item"),
                "url": reverse("admin:forms_radiosheet_add"),
                "description": _(
                    "Capture here news that are broadcast on the radio. The number of newscasts you code will depend on the number of radio channels that broadcast news in your country."
                ),
            },
        ]


class AddTelevisionSubmission(DashboardModule):
    title = _("Television News")
    url = reverse("admin:forms_televisionsheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Television Item"),
                "url": reverse("admin:forms_televisionsheet_add"),
                "description": _(
                    "Capture here news that are broadcast on television. The number of newscast you code will depend on the number of television channels that broadcast news in your country."
                ),
            },
        ]


class AddTwitterSubmission(DashboardModule):
    title = _("Twitter")
    url = reverse("admin:forms_twittersheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Add Tweets"),
                "url": reverse("admin:forms_twittersheet_add"),
                "description": _(
                    "Only capture tweets that are specific posts/feeds by news media on twitter. Remember to capture only national (and if necessary, local) media house Twitter feeds."
                ),
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
