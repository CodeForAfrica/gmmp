from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    columns = 5

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(modules.LinkList(
            _('Add News Subbmission'),
            children=[
            ],
            column=0,
            order=0
        ))
        self.children.append(modules.LinkList(
            _('Add News Subbmission'),
            children=[
            ],
            column=1,
            order=0
        ))
        self.children.append(modules.LinkList(
            _('Add News Subbmission'),
            children=[
            ],
            column=2,
            order=0
        ))
        self.children.append(modules.LinkList(
            _('Add News Subbmission'),
            children=[
            ],
            column=3,
            order=0
        ))
        self.children.append(modules.LinkList(
            _('Add News Subbmission'),
            children=[
            ],
            column=4,
            order=0
        ))
