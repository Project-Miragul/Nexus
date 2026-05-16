import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.utils import Accessor
from .models import LoginAccounts


class LoginServerAccountTable(ExportMixin, tables.Table):
    account_name = tables.TemplateColumn(
        template_name='accounts/account_name_column.html',
        verbose_name='Account Name'
    )
    update = tables.LinkColumn('accounts:update_account',
                               text="Update",
                               args=[Accessor('pk')],
                               attrs={'a': {'class': 'btn fa-regular fa-pen-to-square btn-outline-warning'}},
                               orderable=False)

    class Meta:
        model = LoginAccounts
        template_name = "django_tables2/bootstrap.html"
        fields = ("account_name", "account_email", "created_at", "last_login_date")
        order_by = ("account_name", "created_at")
        orderable = True
