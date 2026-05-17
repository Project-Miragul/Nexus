from datetime import timedelta

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
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
    list_display = ["id", "account_name", "email", "registration_date", "registration_ip_address"]


class ServerListTypeAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ["id", "description"]


class WorldServerRegistrationAdmin(admin.ModelAdmin):
    list_display = ["long_name", "tag_description", "login_server_list_type_id", "is_server_trusted",
                    "login_server_admin_id", "last_login_date"]


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


# ---------------------------------------------------------------------------
# LoginAccountOwnership admin — includes orphan cleanup tool
# ---------------------------------------------------------------------------

class OrphanedFilter(admin.SimpleListFilter):
    title = 'login account status'
    parameter_name = 'orphaned'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Orphaned (login account missing)'),
            ('no', 'Valid (login account exists)'),
        ]

    def queryset(self, request, queryset):
        existing_ids = list(
            LoginAccounts.objects.using('login_server_database').values_list('id', flat=True)
        )
        if self.value() == 'yes':
            return queryset.exclude(login_account_id__in=existing_ids)
        if self.value() == 'no':
            return queryset.filter(login_account_id__in=existing_ids)
        return queryset


class LoginAccountOwnershipAdmin(admin.ModelAdmin):
    change_list_template = 'admin/accounts/loginaccountownership/change_list.html'
    list_display = ['id', 'user', 'login_account_id', 'ls_account_status', 'created_at']
    list_filter = [OrphanedFilter]
    search_fields = ['user__username', 'login_account_id']
    readonly_fields = ['user', 'login_account_id', 'created_at']
    ordering = ['user__username', 'login_account_id']

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'cleanup-orphaned/',
                self.admin_site.admin_view(self.cleanup_orphaned_view),
                name='accounts_loginaccountownership_cleanup',
            ),
            path(
                'ip-conflict-report/',
                self.admin_site.admin_view(self.ip_conflict_report_view),
                name='accounts_loginaccountownership_ip_conflicts',
            ),
        ]
        return custom + urls

    # Batch-load existing LS IDs so the changelist column isn't N+1
    def changelist_view(self, request, extra_context=None):
        existing_ids = set(
            LoginAccounts.objects.using('login_server_database').values_list('id', flat=True)
        )
        request._ls_existing_ids = existing_ids
        orphan_count = LoginAccountOwnership.objects.exclude(
            login_account_id__in=existing_ids
        ).count()
        extra_context = extra_context or {}
        extra_context['orphan_count'] = orphan_count
        extra_context['cleanup_url'] = reverse('admin:accounts_loginaccountownership_cleanup')
        extra_context['ip_conflict_url'] = reverse('admin:accounts_loginaccountownership_ip_conflicts')
        return super().changelist_view(request, extra_context=extra_context)

    def ls_account_status(self, obj):
        existing = getattr(obj, '_ls_existing_ids', None)
        if existing is None:
            exists = LoginAccounts.objects.using('login_server_database').filter(
                id=obj.login_account_id
            ).exists()
        else:
            exists = obj.login_account_id in existing
        if exists:
            return '✓ Exists'
        return '✗ Missing'
    ls_account_status.short_description = 'LS Account'

    def cleanup_orphaned_view(self, request):
        existing_ids = list(
            LoginAccounts.objects.using('login_server_database').values_list('id', flat=True)
        )
        orphaned_qs = LoginAccountOwnership.objects.exclude(login_account_id__in=existing_ids)

        if request.method == 'POST' and request.POST.get('confirmed') == 'yes':
            count = orphaned_qs.count()
            orphaned_qs.delete()
            self.message_user(
                request,
                f'Deleted {count} orphaned LoginAccountOwnership record(s).',
                messages.SUCCESS,
            )
            return HttpResponseRedirect(
                reverse('admin:accounts_loginaccountownership_changelist')
            )

        orphaned_list = list(
            orphaned_qs.select_related('user').values(
                'id', 'user__username', 'login_account_id', 'created_at'
            )
        )
        return TemplateResponse(
            request,
            'admin/accounts/loginaccountownership/cleanup_orphaned.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Clean Up Orphaned Ownership Records',
                'orphaned_list': orphaned_list,
                'orphaned_count': len(orphaned_list),
                'changelist_url': reverse('admin:accounts_loginaccountownership_changelist'),
            },
        )

    def ip_conflict_report_view(self, request):
        from collections import defaultdict

        # Step 1: build ownership map {login_account_id: user}
        ownerships = (
            LoginAccountOwnership.objects
            .select_related('user')
            .values('login_account_id', 'user__id', 'user__username')
        )
        ownership_map = {
            row['login_account_id']: {
                'user_id': row['user__id'],
                'username': row['user__username'],
            }
            for row in ownerships
        }

        if not ownership_map:
            return TemplateResponse(
                request,
                'admin/accounts/loginaccountownership/ip_conflict_report.html',
                {
                    **self.admin_site.each_context(request),
                    'title': 'IP Conflict Report',
                    'flagged_users': [],
                    'changelist_url': reverse('admin:accounts_loginaccountownership_changelist'),
                },
            )

        # Step 2: fetch login account details from LS DB
        ls_accounts = LoginAccounts.objects.using('login_server_database').filter(
            id__in=list(ownership_map.keys())
        ).values('id', 'account_name', 'last_ip_address', 'last_login_date')

        # Step 3: group by (user_id, date) → collect distinct IPs + account rows
        # {user_id: {date: {'username': ..., 'accounts': [...], 'ips': set()}}}
        user_date_map = defaultdict(lambda: defaultdict(lambda: {'accounts': [], 'ips': set(), 'username': ''}))

        for la in ls_accounts:
            owner = ownership_map.get(la['id'])
            if not owner:
                continue
            ip = (la['last_ip_address'] or '').strip()
            login_dt = la['last_login_date']
            if not ip or not login_dt:
                continue
            login_date = login_dt.date() if hasattr(login_dt, 'date') else None
            if not login_date:
                continue
            bucket = user_date_map[owner['user_id']][login_date]
            bucket['username'] = owner['username']
            bucket['ips'].add(ip)
            bucket['accounts'].append({
                'account_name': la['account_name'],
                'ip': ip,
                'last_login_date': login_dt,
            })

        # Step 4: keep only buckets with more than one distinct IP
        flagged_users = []
        for user_id, date_buckets in user_date_map.items():
            for dt, bucket in date_buckets.items():
                if len(bucket['ips']) > 1:
                    bucket['accounts'].sort(key=lambda a: a['last_login_date'])
                    flagged_users.append({
                        'user_id': user_id,
                        'username': bucket['username'],
                        'date': dt,
                        'ips': sorted(bucket['ips']),
                        'accounts': bucket['accounts'],
                    })

        flagged_users.sort(key=lambda r: (r['username'], r['date']))

        return TemplateResponse(
            request,
            'admin/accounts/loginaccountownership/ip_conflict_report.html',
            {
                **self.admin_site.each_context(request),
                'title': 'IP Conflict Report',
                'flagged_users': flagged_users,
                'flagged_count': len(flagged_users),
                'changelist_url': reverse('admin:accounts_loginaccountownership_changelist'),
            },
        )


admin.site.register(LoginAccountOwnership, LoginAccountOwnershipAdmin)
