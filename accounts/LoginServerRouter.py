"""
This is the database router class for operations relating to models belonging to
the login server database.
"""
from accounts.models import LoginAccounts
from accounts.models import ServerAdminRegistration
from accounts.models import ServerListType
from accounts.models import WorldServerRegistration
from accounts.models import (
    LoginAccounts,
    ServerAdminRegistration,
    ServerListType,
    WorldServerRegistration,
    LoginAccountOwnership
)


class LoginServerRouter:
    """
    A router to control all database operations on LoginServer db models in the
    accounts application.
    """

    route_app_labels = {"accounts"}
    login_server_models = [LoginAccounts,
                           ServerAdminRegistration,
                           ServerListType,
                           WorldServerRegistration]

    def db_for_read(self, model, **hints):
        """
        Attempts to read LoginServer models go to the login server database.
        """
        if model._meta.model_name == 'loginaccountownership':
            return 'default'

        if ((model._meta.app_label in self.route_app_labels)
                and (model in self.login_server_models)):
            return "login_server_database"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write LoginServer models go to the login server database.
        """
        if model._meta.model_name == 'loginaccountownership':
            return 'default'

        if ((model._meta.app_label in self.route_app_labels)
                and (model in self.login_server_models)):
            return "login_server_database"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Only allow relations between two login server models
        """
        if (obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels):
            is_ls1 = obj1._meta.model_name in self.login_server_models
            is_ls2 = obj2._meta.model_name in self.login_server_models
            return is_ls1 and is_ls2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            if model_name in self.login_server_models:
                return db == 'login_server_database'
            else:
                # All other models in accounts app (including LoginAccountOwnership)
                return db == 'default'
        return None
