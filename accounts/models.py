from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class WebLoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        ordering = ['-timestamp']


class LoginAccounts(models.Model):
    """
    This model should be tied to the database specified in the LoginServerRouter
    """

    def __str__(self):
        return self.account_name

    id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=50, null=False, unique=True)
    account_password = models.TextField(null=False)
    account_email = models.CharField(max_length=100, null=False)
    source_loginserver = models.CharField(max_length=64, null=True, default=None)
    last_ip_address = models.CharField(max_length=80, null=False)
    last_login_date = models.DateTimeField(null=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "login_accounts"
        verbose_name_plural = "Login Server Accounts"
        managed = False


# Alias so existing imports throughout the project continue to work
LoginServerAccounts = LoginAccounts


class LoginAccountOwnership(models.Model):
    """
    Tracks which website User owns which login server accounts (one-to-many).
    Lives in the default (Django) database — no cross-database FK required.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_login_accounts')
    login_account_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'login_account_id')]


class ServerAdminRegistration(models.Model):
    """
    This model should be tied to the database specified in the LoginServerRouter
    """

    def __str__(self):
        return str(self.ServerAdminID) + " - " + self.AccountName + " - " + self.Email

    ServerAdminID = models.AutoField(primary_key=True, null=False)
    AccountName = models.CharField(max_length=30, null=False)
    AccountPassword = models.CharField(max_length=30, null=False)
    FirstName = models.CharField(max_length=40, null=False)
    LastName = models.CharField(max_length=50, null=False)
    Email = models.EmailField(max_length=100, null=False)
    RegistrationDate = models.DateTimeField(null=False)
    RegistrationIPAddr = models.GenericIPAddressField(max_length=15, null=False)

    class Meta:
        db_table = "tblServerAdminRegistration"
        verbose_name_plural = "Server Admin Registrations"
        managed = False


class ServerListType(models.Model):
    """
    This model should be tied to the database specified in the LoginServerRouter
    """

    def __str__(self):
        return str(self.ServerListTypeID) + " - " + self.ServerListTypeDescription

    ServerListTypeID = models.IntegerField(primary_key=True, null=False)
    ServerListTypeDescription = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "tblServerListType"
        verbose_name_plural = "Server List Types"
        managed = False


class WorldServerRegistration(models.Model):
    """
    This model should be tied to the database specified in the LoginServerRouter
    """

    def __str__(self):
        return str(self.ServerID) + " - " + str(self.ServerLongName) + " - " + str(self.ServerTagDescription)

    ServerID = models.AutoField(primary_key=True, null=False)
    ServerLongName = models.CharField(max_length=100, null=False)
    ServerTagDescription = models.CharField(max_length=50, null=False)
    ServerShortName = models.CharField(max_length=25, null=False)
    ServerListTypeID = models.IntegerField(null=False, default=3)
    ServerLastLoginDate = models.DateField(null=True)
    ServerLastIPAddr = models.GenericIPAddressField(null=True)
    ServerAdminID = models.IntegerField(null=False)
    ServerTrusted = models.IntegerField(null=False)
    Note = models.CharField(max_length=300, null=True)

    class Meta:
        db_table = "tblWorldServerRegistration"
        verbose_name_plural = "World Server Registrations"
        managed = False


class Account(models.Model):
    """
    This model is tied to the GameServerRouter.  It allows us to
    tie a character at char select to a login server account and forum account.
    """

    def __str__(self):
        return str(self.name) + " " + str(self.charname)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, null=False)
    charname = models.CharField(max_length=64, null=False)
    auto_login_charname = models.CharField(max_length=64, null=False)
    sharedplat = models.IntegerField(default=0, null=False)
    password = models.CharField(max_length=50, null=False)
    status = models.IntegerField(default=0, null=False)
    ls_id = models.CharField(max_length=64, null=True, default='eqemu')
    lsaccount_id = models.IntegerField(null=True, default=None)
    gmspeed = models.SmallIntegerField(default=0, null=False)
    invulnerable = models.SmallIntegerField(default=0, null=True)
    flymode = models.SmallIntegerField(default=0, null=True)
    ignore_tells = models.SmallIntegerField(default=0, null=True)
    revoked = models.SmallIntegerField(default=0, null=False)
    karma = models.IntegerField(default=0, null=False)
    minilogin_ip = models.CharField(max_length=32, null=False)
    hideme = models.SmallIntegerField(default=0, null=False)
    rulesflag = models.SmallIntegerField(default=0, null=False)
    suspendeduntil = models.DateTimeField(null=True, blank=True)
    time_creation = models.IntegerField(default=0, null=False)
    ban_reason = models.TextField(null=True, blank=True)
    suspend_reason = models.TextField(null=True, blank=True)
    crc_eqgame = models.TextField(null=True, blank=True)
    crc_skillcaps = models.TextField(null=True, blank=True)
    crc_basedata = models.TextField(null=True, blank=True)
    mule = models.SmallIntegerField(default=0, null=False)

    class Meta:
        db_table = "account"
        managed = False
        permissions = [('can_suspend_accounts', 'Can suspend and lift player game accounts')]

