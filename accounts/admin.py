from datetime import timedelta

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.utils import timezone

from .models import (
    Account,
    LoginAccounts,
    LoginAccountOwnership,
    ServerAdminRegistration,
    ServerListType,
    WorldServerRegistration,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ls_ids_for_users(usernames):
    user_ids = User.objects.filter(username__in=usernames).values_list('id', flat=True)
    return list(
        LoginAccountOwnership.objects.filter(user_id__in=user_ids)
        .values_list('login_account_id', flat=True)
    )


def _game_accounts_qs(ls_ids):
    return Account.objects.using('game_database').filter(lsaccount_id__in=ls_ids)


# ---------------------------------------------------------------------------
# Suspend action
# ---------------------------------------------------------------------------

@admin.action(description='Suspend game accounts…')
def suspend_accounts_action(modeladmin, request, queryset):
    if not request.user.has_perm('accounts.can_suspend_accounts'):
        modeladmin.message_user(request, "You don't have permission to suspend accounts.", messages.ERROR)
        return

    if request.POST.get('confirmed') == 'yes':
        reason = request.POST.get('reason', '').strip() or 'Suspended by admin'
        try:
            duration_days = max(1, int(request.POST.get('duration_days', 7)))
        except (ValueError, TypeError):
            duration_days = 7
        also_disable_web = request.POST.get('disable_web_login') == '1'

        suspended_until = timezone.now() + timedelta(days=duration_days)
        usernames = list(queryset.values_list('username', flat=True))
        ls_ids = _ls_ids_for_users(usernames)
        _game_accounts_qs(ls_ids).update(
            suspendeduntil=suspended_until,
            suspend_reason=reason,
        )

        if also_disable_web:
            queryset.update(is_active=False)

        modeladmin.message_user(
            request,
            f"Suspended game accounts for {queryset.count()} user(s) until "
            f"{suspended_until.strftime('%Y-%m-%d %H:%M UTC')}.",
            messages.SUCCESS,
        )
        return

    # --- Intermediate confirmation page ---
    usernames = list(queryset.values_list('username', flat=True))
    ls_ids = _ls_ids_for_users(usernames)
    game_accounts = list(
        _game_accounts_qs(ls_ids).values('name', 'suspendeduntil', 'suspend_reason')
    )

    return TemplateResponse(request, 'admin/accounts/suspend_confirmation.html', {
        **modeladmin.admin_site.each_context(request),
        'title': 'Suspend Game Accounts',
        'queryset': queryset,
        'game_accounts': game_accounts,
        'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        'action_name': 'suspend_accounts_action',
    })


# ---------------------------------------------------------------------------
# Lift suspension action
# ---------------------------------------------------------------------------

@admin.action(description='Lift suspension early…')
def lift_suspension_action(modeladmin, request, queryset):
    if not request.user.has_perm('accounts.can_suspend_accounts'):
        modeladmin.message_user(request, "You don't have permission to lift suspensions.", messages.ERROR)
        return

    if request.POST.get('confirmed') == 'yes':
        also_restore_web = request.POST.get('restore_web_login') == '1'

        usernames = list(queryset.values_list('username', flat=True))
        ls_ids = _ls_ids_for_users(usernames)
        _game_accounts_qs(ls_ids).update(
            suspendeduntil=timezone.now() - timedelta(seconds=1),
            suspend_reason='',
        )

        if also_restore_web:
            queryset.update(is_active=True)

        modeladmin.message_user(
            request,
            f"Lifted suspension for {queryset.count()} user(s).",
            messages.SUCCESS,
        )
        return

    # --- Intermediate confirmation page ---
    usernames = list(queryset.values_list('username', flat=True))
    ls_ids = _ls_ids_for_users(usernames)
    # Only show accounts that are actually currently suspended
    now = timezone.now()
    game_accounts = list(
        _game_accounts_qs(ls_ids)
        .filter(suspendeduntil__gt=now)
        .values('name', 'suspendeduntil', 'suspend_reason')
    )

    return TemplateResponse(request, 'admin/accounts/lift_suspension_confirmation.html', {
        **modeladmin.admin_site.each_context(request),
        'title': 'Lift Game Account Suspensions',
        'queryset': queryset,
        'game_accounts': game_accounts,
        'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        'action_name': 'lift_suspension_action',
    })


# ---------------------------------------------------------------------------
# Custom User admin with suspension actions
# ---------------------------------------------------------------------------

class CustomUserAdmin(BaseUserAdmin):
    actions = list(BaseUserAdmin.actions or []) + [
        suspend_accounts_action,
        lift_suspension_action,
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ---------------------------------------------------------------------------
# Existing admin registrations
# ---------------------------------------------------------------------------

class LoginAccountsAdmin(admin.ModelAdmin):
    list_display = ["id", "account_name", "account_email", "last_login_date", "source_loginserver"]
    search_fields = ["account_name", "account_email"]
    fieldsets = [
        ("Account", {"fields": ["account_name", "account_password", "account_email"]}),
        ("Login Info", {"fields": ["last_ip_address", "last_login_date", "source_loginserver"]}),
    ]


class ServerAdminRegistrationAdmin(admin.ModelAdmin):
    list_display = ["ServerAdminID", "AccountName", "Email", "RegistrationDate", "RegistrationIPAddr"]


class ServerListTypeAdmin(admin.ModelAdmin):
    ordering = ('ServerListTypeID',)
    list_display = ["ServerListTypeID", "ServerListTypeDescription"]


class WorldServerRegistrationAdmin(admin.ModelAdmin):
    list_display = ["ServerLongName", "ServerTagDescription", "ServerListTypeID", "ServerTrusted", "ServerAdminID",
                    "ServerLastLoginDate"]


class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "lsaccount_id", "charname", "status"]
    list_filter = ["name"]
    search_fields = ["id", "name", "lsaccount_id"]
    readonly_fields = ["id", "karma", "time_creation"]
    fieldsets = [
        ("General Information", {
            "fields": ["name", "charname", "ls_id", "lsaccount_id", "karma", "time_creation"]
        }),
        ("Flag Account as Mule/Trader", {"fields": ["mule"]}),
        ("Administrative Actions",
         {"fields": ["revoked", "ban_reason", "suspendeduntil", "suspend_reason", "rulesflag"]}),
        ("GM Settings", {"fields": ["status", "gmspeed", "hideme", "invulnerable", "flymode", "ignore_tells"]}),
    ]


admin.site.register(LoginAccounts, LoginAccountsAdmin)
admin.site.register(ServerAdminRegistration, ServerAdminRegistrationAdmin)
admin.site.register(ServerListType, ServerListTypeAdmin)
admin.site.register(WorldServerRegistration, WorldServerRegistrationAdmin)
admin.site.register(Account, AccountAdmin)
