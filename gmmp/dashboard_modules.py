from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from jet.dashboard.modules import DashboardModule

from forms.models import (
    InternetNewsSheet,
    NewspaperSheet,
    RadioSheet,
    TelevisionSheet,
    TwitterSheet,
)


class AddInternetNewsSubmission(DashboardModule):
    title = _("Internet")
    url = reverse("admin:forms_internetnewssheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Code Story"),
                "url": reverse("admin:forms_internetnewssheet_add"),
                "description": _('''Code all online news content from the home page or 'first layer' of the site that are not designated as health/sports/entertainment/business news unless it is apparent that they are
uncharacteristically important stories that day (i.e. would appear in the front page section of a newspaper instead of the appropriate sub-section).'''),
            },
        ]


class AddNewspaperSubmission(DashboardModule):
    title = _("Newspapers")
    url = reverse("admin:forms_newspapersheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Code Story"),
                "url": reverse("admin:forms_newspapersheet_add"),
                "description": _('''Begin with the main news page (usually Page 1). Code all the news stories on this page. Then go to the next major news page.
Code regular news stories only - not editorials, commentaries, letters to the editor.'''),
            },
        ]


class AddRadioSubmission(DashboardModule):
    title = _("Radio")
    url = reverse("admin:forms_radiosheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Code Story"),
                "url": reverse("admin:forms_radiosheet_add"),
                "description": _('''Code all the stories in the newscasts that you selected, including: All types of news — politics, local stories, international stories, reports on education, medicine, business, entertainment, and so on.
Sports reports — code only if they are part of the newscast. (Do not code a programme if it is
entirely about sports.)'''),
            },
        ]


class AddTelevisionSubmission(DashboardModule):
    title = _("Television")
    url = reverse("admin:forms_televisionsheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Code Story"),
                "url": reverse("admin:forms_televisionsheet_add"),
                "description": _('''Code all the stories in the newscasts that you selected, including: All types of news — politics, local stories, international stories, reports on education, medicine, business, entertainment, and so on.
Sports reports — code only if they are part of the newscast. (Do not code a programme if it is
entirely about sports.)'''),
            },
        ]


class AddTwitterSubmission(DashboardModule):
    title = _("Twitter")
    url = reverse("admin:forms_twittersheet_add")
    template = "gmmp/dashboard_modules/add_submission.html"

    def init_with_context(self, context):
        self.children = [
            {
                "title": _("Code Tweet"),
                "url": reverse("admin:forms_twittersheet_add"),
                "description": _('''Begin coding after 6.30 p.m. on the global monitoring day. Code every third tweet time stamped 6.30 p.m. or earlier published on the media monitoring day up to 15 – 20 tweets. If the Twitter news feed provider you have chosen does not yield 15 to 20 Tweets by taking every third item, take every second item. If they provide less than 15 tweets per day, they are not appropriate for inclusion in the monitoring.'''),
            },
        ]


class Submissions(DashboardModule):
    title = "Coded"
    template = "gmmp/dashboard_modules/submissions.html"

    def init_with_context(self, context):
        self.children = [
            {
                "name": _("Newspapers"),
                "count": NewspaperSheet.objects.count(),
                "url": reverse("admin:forms_newspapersheet_changelist"),
            },
            {
                "name": _("Radio"),
                "count": RadioSheet.objects.count(),
                "url": reverse("admin:forms_radiosheet_changelist"),
            },
            {
                "name": _("Television"),
                "count": TelevisionSheet.objects.count(),
                "url": reverse("admin:forms_televisionsheet_changelist"),
            },
            {
                "name": _("Internet"),
                "count": InternetNewsSheet.objects.count(),
                "url": reverse("admin:forms_internetnewssheet_changelist"),
            },
            {
                "name": _("Twitter"),
                "count": TwitterSheet.objects.count(),
                "url": reverse("admin:forms_twittersheet_changelist"),
            },
        ]
