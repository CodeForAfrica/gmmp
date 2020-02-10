from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard

from gmmp.dashboard_modules import AddInternetNewsSubmission, AddNewspaperSubmission, AddRadioSubmission, AddTelevisionSubmission, AddTwitterSubmission

class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(AddNewspaperSubmission(
            column=0,
            order=0
        ))
        self.children.append(AddRadioSubmission(
            column=1,
            order=0
        ))
        self.children.append(AddTelevisionSubmission(
            column=2,
            order=0
        ))
        self.children.append(AddInternetNewsSubmission(
            column=0,
            order=1
        ))
        self.children.append(AddTwitterSubmission(
            column=1,
            order=1
        ))
        self.children.append(modules.LinkList(
            _('Add News Subbmission'),
            children=[
            ],
            column=4,
            order=0
        ))
