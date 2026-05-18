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
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_login_accounts')
    login_account_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'login_account_id')]
        db_table = "accounts_loginaccountownership"  # optional but clear
        # Force this model to always use the default database
        app_label = 'accounts'

    def __str__(self):
        return f"User {self.user_id} owns login account {self.login_account_id}"


class ServerAdminRegistration(models.Model):
    """
    This model maps to the login_server_admins table in the login server database.
    """

    def __str__(self):
        return f"{self.id} - {self.account_name} - {self.email}"

    id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=30, null=False)
    account_password = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=100, null=False)
    registration_date = models.DateTimeField(null=False)
    registration_ip_address = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = "login_server_admins"
        verbose_name_plural = "Server Admin Registrations"
        managed = False


class ServerListType(models.Model):
    """
    This model maps to the login_server_list_types table in the login server database.
    """

    def __str__(self):
        return f"{self.id} - {self.description}"

    id = models.PositiveIntegerField(primary_key=True)
    description = models.CharField(max_length=60, null=False)

    class Meta:
        db_table = "login_server_list_types"
        verbose_name_plural = "Server List Types"
        managed = False


class WorldServerRegistration(models.Model):
    """
    This model maps to the login_world_servers table in the login server database.
    """

    def __str__(self):
        return f"{self.id} - {self.long_name} - {self.tag_description}"

    id = models.AutoField(primary_key=True)
    long_name = models.CharField(max_length=100, null=False)
    short_name = models.CharField(max_length=100, null=False)
    tag_description = models.CharField(max_length=50, null=False, default='')
    login_server_list_type_id = models.IntegerField(null=False, default=3)
    last_login_date = models.DateTimeField(null=True, blank=True)
    last_ip_address = models.CharField(max_length=80, null=True, blank=True)
    login_server_admin_id = models.IntegerField(null=False)
    is_server_trusted = models.IntegerField(null=False)
    note = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "login_world_servers"
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
#    mule = models.SmallIntegerField(default=0, null=False)

    class Meta:
        db_table = "account"
        managed = False
        permissions = [('can_suspend_accounts', 'Can suspend and lift player game accounts')]


class IpExemption(models.Model):
    """
    Maps to the ip_exemptions table in the game database.
    An entry here means the given IP is allowed exemption_amount concurrent connections
    instead of the server default box limit.
    """
    exemption_id = models.AutoField(primary_key=True)
    exemption_ip = models.CharField(max_length=255, null=True, blank=True)
    exemption_amount = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "ip_exemptions"
        managed = False


class RuleValues(models.Model):
    """
    Maps to the rule_values table in the game database.
    Stores server configuration rules as name/value pairs.
    """
    ruleset_id = models.IntegerField(default=0)
    rule_name = models.CharField(max_length=255, primary_key=True)
    rule_value = models.CharField(max_length=30, null=False)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "rule_values"
        managed = False


class AccountIp(models.Model):
    """
    Maps to the account_ip table in the game database.
    Tracks every IP address a game account has connected from, with a hit count
    and the last time that IP was used.  Composite PK (accid + ip).
    """
    accid = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=32)
    count = models.IntegerField(default=1)
    lastused = models.DateTimeField()

    class Meta:
        db_table = "account_ip"
        managed = False
        unique_together = [('accid', 'ip')]


class PlayerEventLog(models.Model):
    """
    Maps to the player_event_logs table in the game database.
    Stores structured player events; event_data is a JSON string whose
    schema varies by event_type_id.
    """
    id = models.BigAutoField(primary_key=True)
    account_id = models.BigIntegerField(null=True, blank=True)
    character_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    zone_id = models.IntegerField(null=True, blank=True)
    instance_id = models.IntegerField(null=True, blank=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    z = models.FloatField(null=True, blank=True)
    heading = models.FloatField(null=True, blank=True)
    event_type_id = models.IntegerField(null=True, blank=True, db_index=True)
    event_type_name = models.CharField(max_length=255, null=True, blank=True)
    event_data = models.TextField(null=True, blank=True)
    etl_table_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "player_event_logs"
        managed = False

