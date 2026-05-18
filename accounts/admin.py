from datetime import timedelta

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone

from common.models.characters import Characters
from common.models.guilds import Guilds, GuildMembers
from .forms import LoginAccountOwnershipAdminForm
from .models import (
    Account,
    AccountIp,
    IpExemption,
    LoginAccounts,
    LoginAccountOwnership,
    PlayerEventLog,
    RuleValues,
    ServerAdminRegistration,
    ServerListType,
    WebLoginHistory,
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
# Ban / unban actions
# ---------------------------------------------------------------------------

@admin.action(description='Permanently ban game accounts…')
def ban_accounts_action(modeladmin, request, queryset):
    if not request.user.has_perm('accounts.can_suspend_accounts'):
        modeladmin.message_user(request, "You don't have permission to ban accounts.", messages.ERROR)
        return

    if request.POST.get('confirmed') == 'yes':
        reason = request.POST.get('reason', '').strip() or 'Banned by admin'
        also_disable_web = request.POST.get('disable_web_login') == '1'

        usernames = list(queryset.values_list('username', flat=True))
        ls_ids = _ls_ids_for_users(usernames)
        _game_accounts_qs(ls_ids).update(revoked=1, ban_reason=reason)

        if also_disable_web:
            queryset.update(is_active=False)

        modeladmin.message_user(
            request,
            f"Permanently banned game accounts for {queryset.count()} user(s).",
            messages.SUCCESS,
        )
        return

    usernames = list(queryset.values_list('username', flat=True))
    ls_ids = _ls_ids_for_users(usernames)
    game_accounts = list(
        _game_accounts_qs(ls_ids).values('name', 'revoked', 'ban_reason')
    )

    return TemplateResponse(request, 'admin/accounts/ban_confirmation.html', {
        **modeladmin.admin_site.each_context(request),
        'title': 'Permanently Ban Game Accounts',
        'queryset': queryset,
        'game_accounts': game_accounts,
        'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        'action_name': 'ban_accounts_action',
    })


@admin.action(description='Lift permanent ban…')
def lift_ban_action(modeladmin, request, queryset):
    if not request.user.has_perm('accounts.can_suspend_accounts'):
        modeladmin.message_user(request, "You don't have permission to lift bans.", messages.ERROR)
        return

    if request.POST.get('confirmed') == 'yes':
        also_restore_web = request.POST.get('restore_web_login') == '1'

        usernames = list(queryset.values_list('username', flat=True))
        ls_ids = _ls_ids_for_users(usernames)
        _game_accounts_qs(ls_ids).update(revoked=0, ban_reason='')

        if also_restore_web:
            queryset.update(is_active=True)

        modeladmin.message_user(
            request,
            f"Lifted permanent ban for {queryset.count()} user(s).",
            messages.SUCCESS,
        )
        return

    usernames = list(queryset.values_list('username', flat=True))
    ls_ids = _ls_ids_for_users(usernames)
    game_accounts = list(
        _game_accounts_qs(ls_ids)
        .filter(revoked=1)
        .values('name', 'ban_reason')
    )

    return TemplateResponse(request, 'admin/accounts/lift_ban_confirmation.html', {
        **modeladmin.admin_site.each_context(request),
        'title': 'Lift Permanent Ban',
        'queryset': queryset,
        'game_accounts': game_accounts,
        'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        'action_name': 'lift_ban_action',
    })


# ---------------------------------------------------------------------------
# Custom User admin with suspension actions
# ---------------------------------------------------------------------------

class CustomUserAdmin(BaseUserAdmin):
    change_list_template = 'admin/accounts/user/change_list.html'
    actions = list(BaseUserAdmin.actions or []) + [
        suspend_accounts_action,
        lift_suspension_action,
        ban_accounts_action,
        lift_ban_action,
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'character-map/',
                self.admin_site.admin_view(self.character_map_view),
                name='accounts_user_character_map',
            ),
            path(
                'shared-email/',
                self.admin_site.admin_view(self.shared_email_report_view),
                name='accounts_user_shared_email',
            ),
            path(
                'high-velocity/',
                self.admin_site.admin_view(self.high_velocity_view),
                name='accounts_user_high_velocity',
            ),
            path(
                'mfa-status/',
                self.admin_site.admin_view(self.mfa_status_view),
                name='accounts_user_mfa_status',
            ),
            path(
                'quick-action/<int:user_id>/<str:action_type>/',
                self.admin_site.admin_view(self.quick_action_view),
                name='accounts_user_quick_action',
            ),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['character_map_url'] = reverse('admin:accounts_user_character_map')
        extra_context['shared_email_url'] = reverse('admin:accounts_user_shared_email')
        extra_context['high_velocity_url'] = reverse('admin:accounts_user_high_velocity')
        extra_context['mfa_status_url'] = reverse('admin:accounts_user_mfa_status')
        return super().changelist_view(request, extra_context=extra_context)

    def character_map_view(self, request):
        from django.contrib.auth.models import User as AuthUser
        from datetime import datetime, timezone as dt_timezone

        query = request.GET.get('q', '').strip()
        results = []
        unlinked_results = []
        searched = False

        if query:
            searched = True

            # Accumulate {user_id: [reason, ...]} across all search paths.
            # Using a list+dedup so insertion order is preserved for display.
            match_reasons = {}

            def add_reason(uid, reason):
                reasons = match_reasons.setdefault(uid, [])
                if reason not in reasons:
                    reasons.append(reason)

            # ------------------------------------------------------------------
            # Path 1: web username
            # ------------------------------------------------------------------
            for u in AuthUser.objects.filter(username__icontains=query).values('id', 'username'):
                add_reason(u['id'], f"web user: {u['username']}")

            # ------------------------------------------------------------------
            # Path 2: login account name  (LS DB → ownership → user)
            # ------------------------------------------------------------------
            ls_name_matches = list(
                LoginAccounts.objects.using('login_server_database')
                .filter(account_name__icontains=query)
                .values('id', 'account_name')
            )
            ls_name_map = {m['id']: m['account_name'] for m in ls_name_matches}
            if ls_name_map:
                for o in LoginAccountOwnership.objects.filter(
                    login_account_id__in=ls_name_map.keys()
                ).values('user_id', 'login_account_id'):
                    add_reason(o['user_id'], f"login account: {ls_name_map[o['login_account_id']]}")

            # ------------------------------------------------------------------
            # Path 3: world account name  (game DB → ownership → user)
            # ------------------------------------------------------------------
            wa_name_matches = list(
                Account.objects.using('game_database')
                .filter(name__icontains=query)
                .values('id', 'name', 'lsaccount_id')
            )
            if wa_name_matches:
                wa_lsid_to_name = {
                    m['lsaccount_id']: m['name']
                    for m in wa_name_matches if m['lsaccount_id']
                }
                linked_lsids = set()
                for o in LoginAccountOwnership.objects.filter(
                    login_account_id__in=wa_lsid_to_name.keys()
                ).values('user_id', 'login_account_id'):
                    add_reason(o['user_id'], f"world account: {wa_lsid_to_name[o['login_account_id']]}")
                    linked_lsids.add(o['login_account_id'])
                # World accounts with no web user
                seen_wa_ids = set()
                for m in wa_name_matches:
                    if m['lsaccount_id'] not in linked_lsids and m['id'] not in seen_wa_ids:
                        seen_wa_ids.add(m['id'])
                        unlinked_results.append({
                            'type': 'world_account',
                            'name': m['name'],
                            'id': m['id'],
                            'lsaccount_id': m['lsaccount_id'],
                        })

            # ------------------------------------------------------------------
            # Path 4: character name  (game DB → world account → ownership → user)
            # ------------------------------------------------------------------
            char_matches = list(
                Characters.objects.using('game_database')
                .filter(name__icontains=query)
                .values('id', 'name', 'account_id', 'level')
            )
            if char_matches:
                chars_per_account = {}
                for c in char_matches:
                    chars_per_account.setdefault(c['account_id'], []).append(c['name'])

                wa_for_chars = list(
                    Account.objects.using('game_database')
                    .filter(id__in=chars_per_account.keys())
                    .values('id', 'lsaccount_id')
                )
                lsid_to_acc_ids = {}
                for wa in wa_for_chars:
                    if wa['lsaccount_id']:
                        lsid_to_acc_ids.setdefault(wa['lsaccount_id'], []).append(wa['id'])

                linked_lsids = set()
                for o in LoginAccountOwnership.objects.filter(
                    login_account_id__in=lsid_to_acc_ids.keys()
                ).values('user_id', 'login_account_id'):
                    for acc_id in lsid_to_acc_ids.get(o['login_account_id'], []):
                        for cname in chars_per_account.get(acc_id, []):
                            add_reason(o['user_id'], f"character: {cname}")
                    linked_lsids.add(o['login_account_id'])

                # Characters whose world account has no web user
                seen_char_acc_ids = set()
                for wa in wa_for_chars:
                    if wa['lsaccount_id'] not in linked_lsids and wa['id'] not in seen_char_acc_ids:
                        seen_char_acc_ids.add(wa['id'])
                        for cname in chars_per_account.get(wa['id'], []):
                            unlinked_results.append({
                                'type': 'character',
                                'name': cname,
                                'account_id': wa['id'],
                                'lsaccount_id': wa['lsaccount_id'],
                            })

            # ------------------------------------------------------------------
            # Assemble full tree for every matched user
            # ------------------------------------------------------------------
            if match_reasons:
                all_user_ids = list(match_reasons.keys())
                users = list(
                    AuthUser.objects.filter(id__in=all_user_ids)
                    .values('id', 'username', 'email', 'is_active')
                )

                ownerships = list(
                    LoginAccountOwnership.objects
                    .filter(user_id__in=all_user_ids)
                    .values('user_id', 'login_account_id')
                )
                ownership_by_user = {}
                for o in ownerships:
                    ownership_by_user.setdefault(o['user_id'], []).append(o['login_account_id'])

                all_ls_ids = [o['login_account_id'] for o in ownerships]
                ls_accounts = {}
                if all_ls_ids:
                    for la in LoginAccounts.objects.using('login_server_database').filter(
                        id__in=all_ls_ids
                    ).values('id', 'account_name'):
                        ls_accounts[la['id']] = la['account_name']

                world_accounts = {}
                if all_ls_ids:
                    for wa in Account.objects.using('game_database').filter(
                        lsaccount_id__in=all_ls_ids
                    ).values('id', 'name', 'lsaccount_id', 'status', 'revoked'):
                        world_accounts.setdefault(wa['lsaccount_id'], []).append(wa)

                world_account_ids = [wa['id'] for was in world_accounts.values() for wa in was]
                characters_by_account = {}
                if world_account_ids:
                    for ch in Characters.objects.using('game_database').filter(
                        account_id__in=world_account_ids
                    ).values('id', 'name', 'account_id', 'level', 'race', 'class_name', 'last_login'):
                        ts = ch['last_login']
                        ch['last_login_dt'] = (
                            datetime.fromtimestamp(ts, tz=dt_timezone.utc) if ts else None
                        )
                        characters_by_account.setdefault(ch['account_id'], []).append(ch)

                for user in users:
                    ls_ids_for_user = ownership_by_user.get(user['id'], [])
                    login_accounts = []
                    for ls_id in ls_ids_for_user:
                        enriched_world = []
                        for wa in world_accounts.get(ls_id, []):
                            chars = sorted(
                                characters_by_account.get(wa['id'], []),
                                key=lambda c: -c['level'],
                            )
                            enriched_world.append({**wa, 'characters': chars})
                        login_accounts.append({
                            'ls_id': ls_id,
                            'ls_account_name': ls_accounts.get(ls_id, f'(id={ls_id})'),
                            'world_accounts': enriched_world,
                        })
                    results.append({
                        'user': user,
                        'login_accounts': login_accounts,
                        'match_reasons': match_reasons.get(user['id'], []),
                    })

                results.sort(key=lambda r: r['user']['username'])

        return TemplateResponse(
            request,
            'admin/accounts/user/character_map.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Character Map',
                'query': query,
                'results': results,
                'unlinked_results': unlinked_results,
                'searched': searched,
                'changelist_url': reverse('admin:auth_user_changelist'),
            },
        )

    def quick_action_view(self, request, user_id, action_type):
        from django.contrib.auth.models import User as AuthUser
        from django.shortcuts import get_object_or_404

        VALID_ACTIONS = ('suspend', 'lift-suspension', 'ban', 'lift-ban')
        if action_type not in VALID_ACTIONS:
            from django.http import Http404
            raise Http404

        if not request.user.has_perm('accounts.can_suspend_accounts'):
            self.message_user(request, "You don't have permission to perform this action.", messages.ERROR)
            return HttpResponseRedirect(reverse('admin:accounts_user_character_map'))

        user = get_object_or_404(AuthUser, pk=user_id)
        return_url = reverse('admin:accounts_user_character_map') + f'?q={user.username}'
        now = timezone.now()

        ls_ids = _ls_ids_for_users([user.username])
        game_accounts = list(
            _game_accounts_qs(ls_ids)
            .values('id', 'name', 'revoked', 'ban_reason', 'suspendeduntil', 'suspend_reason')
        )

        if request.method == 'POST':
            reason = request.POST.get('reason', '').strip() or f'Action by admin'
            toggle_web = request.POST.get('toggle_web') == '1'

            if action_type == 'suspend':
                try:
                    duration_days = max(1, int(request.POST.get('duration_days', 7)))
                except (ValueError, TypeError):
                    duration_days = 7
                _game_accounts_qs(ls_ids).update(
                    suspendeduntil=now + timedelta(days=duration_days),
                    suspend_reason=reason,
                )
                if toggle_web:
                    user.is_active = False
                    user.save()
            elif action_type == 'lift-suspension':
                _game_accounts_qs(ls_ids).update(
                    suspendeduntil=now - timedelta(seconds=1),
                    suspend_reason='',
                )
                if toggle_web:
                    user.is_active = True
                    user.save()
            elif action_type == 'ban':
                _game_accounts_qs(ls_ids).update(revoked=1, ban_reason=reason)
                if toggle_web:
                    user.is_active = False
                    user.save()
            elif action_type == 'lift-ban':
                _game_accounts_qs(ls_ids).update(revoked=0, ban_reason='')
                if toggle_web:
                    user.is_active = True
                    user.save()

            self.message_user(
                request,
                f"Applied '{action_type}' for {user.username}.",
                messages.SUCCESS,
            )
            return HttpResponseRedirect(return_url)

        return TemplateResponse(
            request,
            'admin/accounts/user/quick_action.html',
            {
                **self.admin_site.each_context(request),
                'title': f'{action_type.replace("-", " ").title()} — {user.username}',
                'action_user': user,
                'action_type': action_type,
                'game_accounts': game_accounts,
                'return_url': return_url,
                'now': now,
            },
        )

    def shared_email_report_view(self, request):
        from django.contrib.auth.models import User as AuthUser
        from django.db.models import Count

        # Find emails used by more than one account (exclude blank)
        dupes = (
            AuthUser.objects
            .exclude(email='')
            .values('email')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
            .order_by('-count', 'email')
        )

        email_groups = []
        for row in dupes:
            users = list(
                AuthUser.objects
                .filter(email=row['email'])
                .values('id', 'username', 'email', 'is_active', 'date_joined')
                .order_by('date_joined')
            )
            email_groups.append({'email': row['email'], 'count': row['count'], 'users': users})

        return TemplateResponse(
            request,
            'admin/accounts/user/shared_email_report.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Shared Email Report',
                'email_groups': email_groups,
                'flagged_count': len(email_groups),
                'changelist_url': reverse('admin:auth_user_changelist'),
            },
        )

    def high_velocity_view(self, request):
        from django.contrib.auth.models import User as AuthUser
        from django.db.models import Count
        from django.db.models.functions import TruncDate

        DEFAULT_THRESHOLD = 3
        try:
            threshold = max(1, int(request.GET.get('threshold', DEFAULT_THRESHOLD)))
        except (ValueError, TypeError):
            threshold = DEFAULT_THRESHOLD

        # Days where threshold+ accounts were created
        busy_days = (
            AuthUser.objects
            .annotate(day=TruncDate('date_joined'))
            .values('day')
            .annotate(count=Count('id'))
            .filter(count__gte=threshold)
            .order_by('-day')
        )

        day_groups = []
        for row in busy_days:
            users = list(
                AuthUser.objects
                .filter(date_joined__date=row['day'])
                .values('id', 'username', 'email', 'is_active', 'date_joined')
                .order_by('date_joined')
            )
            day_groups.append({'day': row['day'], 'count': row['count'], 'users': users})

        return TemplateResponse(
            request,
            'admin/accounts/user/high_velocity_report.html',
            {
                **self.admin_site.each_context(request),
                'title': 'High Velocity New Accounts',
                'day_groups': day_groups,
                'flagged_count': len(day_groups),
                'threshold': threshold,
                'default_threshold': DEFAULT_THRESHOLD,
                'changelist_url': reverse('admin:auth_user_changelist'),
            },
        )

    def mfa_status_view(self, request):
        from django.contrib.auth.models import User as AuthUser
        from django_otp.plugins.otp_totp.models import TOTPDevice
        from django_otp.plugins.otp_static.models import StaticDevice

        # Users with at least one confirmed TOTP or WebAuthn device
        totp_user_ids = set(
            TOTPDevice.objects.filter(confirmed=True).values_list('user_id', flat=True)
        )
        static_user_ids = set(
            StaticDevice.objects.filter(confirmed=True).values_list('user_id', flat=True)
        )
        webauthn_user_ids = set()
        try:
            from django_otp_webauthn.models import WebAuthnCredential
            webauthn_user_ids = set(
                WebAuthnCredential.objects.values_list('user_id', flat=True)
            )
        except Exception:
            pass

        mfa_user_ids = totp_user_ids | static_user_ids | webauthn_user_ids

        all_users = list(
            AuthUser.objects
            .values('id', 'username', 'email', 'is_active', 'date_joined', 'last_login')
            .order_by('username')
        )

        for u in all_users:
            uid = u['id']
            methods = []
            if uid in totp_user_ids:
                methods.append('TOTP')
            if uid in webauthn_user_ids:
                methods.append('Passkey')
            if uid in static_user_ids and uid not in totp_user_ids and uid not in webauthn_user_ids:
                methods.append('Backup codes only')
            u['mfa_methods'] = methods
            u['has_mfa'] = uid in mfa_user_ids

        enrolled = [u for u in all_users if u['has_mfa']]
        not_enrolled = [u for u in all_users if not u['has_mfa']]

        return TemplateResponse(
            request,
            'admin/accounts/user/mfa_status_report.html',
            {
                **self.admin_site.each_context(request),
                'title': 'MFA Status Report',
                'enrolled': enrolled,
                'not_enrolled': not_enrolled,
                'enrolled_count': len(enrolled),
                'not_enrolled_count': len(not_enrolled),
                'total': len(all_users),
                'changelist_url': reverse('admin:auth_user_changelist'),
            },
        )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ---------------------------------------------------------------------------
# Existing admin registrations
# ---------------------------------------------------------------------------

class LoginAccountsAdmin(admin.ModelAdmin):
    list_display = ["id", "account_name", "account_email", "last_login_date", "source_loginserver", "created_at"]
    search_fields = ["=id", "account_name", "account_email"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        ("Account", {"fields": ["account_name", "account_password", "account_email"]}),
        ("Login Info", {"fields": ["last_ip_address", "last_login_date", "source_loginserver"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]


class ServerAdminRegistrationAdmin(admin.ModelAdmin):
    list_display = ["id", "account_name", "first_name", "last_name", "email", "registration_date", "registration_ip_address"]
    search_fields = ["account_name", "email", "first_name", "last_name"]


class ServerListTypeAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ["id", "description"]


class WorldServerRegistrationAdmin(admin.ModelAdmin):
    list_display = ["long_name", "short_name", "tag_description", "login_server_list_type_id",
                    "is_server_trusted", "login_server_admin_id", "last_login_date", "last_ip_address"]
    search_fields = ["long_name", "short_name", "tag_description"]
    readonly_fields = ["last_login_date", "last_ip_address"]
    fieldsets = [
        ("Identity", {"fields": ["long_name", "short_name", "tag_description", "note"]}),
        ("Configuration", {"fields": ["login_server_list_type_id", "login_server_admin_id", "is_server_trusted"]}),
        ("Connection", {"fields": ["last_login_date", "last_ip_address"], "classes": ["collapse"]}),
    ]


admin.site.register(LoginAccounts, LoginAccountsAdmin)
admin.site.register(ServerAdminRegistration, ServerAdminRegistrationAdmin)
admin.site.register(ServerListType, ServerListTypeAdmin)
admin.site.register(WorldServerRegistration, WorldServerRegistrationAdmin)


# ---------------------------------------------------------------------------
# Web login history — read-only audit log
# ---------------------------------------------------------------------------

class WebLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'ip_address']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'timestamp', 'ip_address']
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(WebLoginHistory, WebLoginHistoryAdmin)


# ---------------------------------------------------------------------------
# Account (world server) admin — with suspended accounts dashboard
# ---------------------------------------------------------------------------

class AccountAdmin(admin.ModelAdmin):
    change_list_template = 'admin/accounts/account/change_list.html'
    list_display = ["name", "id", "lsaccount_id", "ls_id", "charname", "status", "revoked", "time_creation_display"]
    list_filter = ["revoked", "status"]
    search_fields = ["id", "name", "lsaccount_id"]
    readonly_fields = ["id", "karma", "time_creation", "time_creation_display"]
    fieldsets = [
        ("General Information", {
            "fields": ["name", "charname", "auto_login_charname", "ls_id", "lsaccount_id",
                       "sharedplat", "karma", "time_creation_display"]
        }),
        ("Administrative Actions",
         {"fields": ["revoked", "ban_reason", "suspendeduntil", "suspend_reason", "rulesflag"]}),
        ("GM Settings", {"fields": ["status", "gmspeed", "hideme", "invulnerable", "flymode", "ignore_tells"]}),
        ("Network", {"fields": ["minilogin_ip"], "classes": ["collapse"]}),
    ]

    def time_creation_display(self, obj):
        if not obj.time_creation:
            return '—'
        from datetime import datetime, timezone as dt_timezone
        return datetime.fromtimestamp(obj.time_creation, tz=dt_timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    time_creation_display.short_description = 'Created (UTC)'
    time_creation_display.admin_order_field = 'time_creation'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'suspended-dashboard/',
                self.admin_site.admin_view(self.suspended_dashboard_view),
                name='accounts_account_suspended_dashboard',
            ),
            path(
                'record-counts/',
                self.admin_site.admin_view(self.record_count_dashboard_view),
                name='accounts_account_record_counts',
            ),
            path(
                'item-history/',
                self.admin_site.admin_view(self.item_history_view),
                name='accounts_account_item_history',
            ),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        suspended_count = (
            Account.objects.using('game_database')
            .filter(suspendeduntil__gt=timezone.now())
            .count()
        )
        extra_context = extra_context or {}
        extra_context['suspended_count'] = suspended_count
        extra_context['suspended_dashboard_url'] = reverse('admin:accounts_account_suspended_dashboard')
        extra_context['record_counts_url'] = reverse('admin:accounts_account_record_counts')
        extra_context['item_history_url'] = reverse('admin:accounts_account_item_history')
        return super().changelist_view(request, extra_context=extra_context)

    def suspended_dashboard_view(self, request):
        now = timezone.now()
        suspended = list(
            Account.objects.using('game_database')
            .filter(suspendeduntil__gt=now)
            .values('id', 'name', 'lsaccount_id', 'suspendeduntil', 'suspend_reason', 'status')
            .order_by('suspendeduntil')
        )

        # Resolve web users via LoginAccountOwnership (default DB)
        lsaccount_ids = [a['lsaccount_id'] for a in suspended if a['lsaccount_id']]
        ownerships = (
            LoginAccountOwnership.objects
            .filter(login_account_id__in=lsaccount_ids)
            .select_related('user')
            .values('login_account_id', 'user__username', 'user__id')
        )
        web_user_map = {o['login_account_id']: o['user__username'] for o in ownerships}

        for acct in suspended:
            acct['web_username'] = web_user_map.get(acct['lsaccount_id'], '—')

        return TemplateResponse(
            request,
            'admin/accounts/account/suspended_dashboard.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Suspended Accounts',
                'suspended': suspended,
                'suspended_count': len(suspended),
                'changelist_url': reverse('admin:accounts_account_changelist'),
            },
        )


    def item_history_view(self, request):
        import json

        char_query = request.GET.get('q', '').strip()
        item_query = request.GET.get('item', '').strip()
        searched = bool(char_query or item_query)
        results = []
        error = None

        if searched:
            # Resolve character names → IDs from game DB
            char_qs = Characters.objects.using('game_database')
            if char_query:
                char_qs = char_qs.filter(name__icontains=char_query)
            char_map = {c['id']: c['name'] for c in char_qs.values('id', 'name')}

            if not char_map and char_query:
                error = f'No characters found matching "{char_query}".'
            else:
                log_qs = (
                    PlayerEventLog.objects.using('game_database')
                    .filter(event_type_id=47)
                    .order_by('-created_at')
                )
                if char_map:
                    log_qs = log_qs.filter(character_id__in=char_map.keys())
                if item_query:
                    log_qs = log_qs.filter(event_data__icontains=item_query)

                for row in log_qs.values(
                    'id', 'character_id', 'zone_id', 'event_data', 'created_at'
                )[:500]:
                    try:
                        data = json.loads(row['event_data'] or '{}')
                    except (ValueError, TypeError):
                        data = {}
                    results.append({
                        'character_id': row['character_id'],
                        'character_name': char_map.get(row['character_id'], f'(id={row["character_id"]})'),
                        'item_id': data.get('item_id'),
                        'item_name': data.get('item_name', '—'),
                        'to_slot': data.get('to_slot'),
                        'charges': data.get('charges', 0),
                        'zone_id': row['zone_id'],
                        'created_at': row['created_at'],
                    })

        return TemplateResponse(
            request,
            'admin/accounts/account/item_history.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Item History',
                'char_query': char_query,
                'item_query': item_query,
                'results': results,
                'result_count': len(results),
                'searched': searched,
                'error': error,
                'changelist_url': reverse('admin:accounts_account_changelist'),
            },
        )

    def record_count_dashboard_view(self, request):
        from django.contrib.auth.models import User as AuthUser

        counts = {
            'web_users': AuthUser.objects.count(),
            'ownerships': LoginAccountOwnership.objects.count(),
            'login_accounts': LoginAccounts.objects.using('login_server_database').count(),
            'world_accounts': Account.objects.using('game_database').count(),
            'characters': Characters.objects.using('game_database').count(),
            'guilds': Guilds.objects.using('game_database').count(),
            'guild_members': GuildMembers.objects.using('game_database').count(),
        }

        return TemplateResponse(
            request,
            'admin/accounts/account/record_count_dashboard.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Record Counts',
                'counts': counts,
                'changelist_url': reverse('admin:accounts_account_changelist'),
            },
        )


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
    ordering = ['user__username', 'login_account_id']

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = LoginAccountOwnershipAdminForm
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Existing record — lock the core fields to prevent accidental edits
            return ['user', 'login_account_id', 'created_at']
        return ['created_at']

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
            path(
                'shared-ip-report/',
                self.admin_site.admin_view(self.shared_ip_report_view),
                name='accounts_loginaccountownership_shared_ip',
            ),
            path(
                'unlinked-report/',
                self.admin_site.admin_view(self.unlinked_report_view),
                name='accounts_loginaccountownership_unlinked',
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
        linked_ids = set(
            LoginAccountOwnership.objects.values_list('login_account_id', flat=True)
        )
        unlinked_count = len(existing_ids - linked_ids)
        extra_context = extra_context or {}
        extra_context['orphan_count'] = orphan_count
        extra_context['unlinked_count'] = unlinked_count
        extra_context['cleanup_url'] = reverse('admin:accounts_loginaccountownership_cleanup')
        extra_context['ip_conflict_url'] = reverse('admin:accounts_loginaccountownership_ip_conflicts')
        extra_context['shared_ip_url'] = reverse('admin:accounts_loginaccountownership_shared_ip')
        extra_context['unlinked_url'] = reverse('admin:accounts_loginaccountownership_unlinked')
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


    def shared_ip_report_view(self, request):
        from collections import defaultdict

        DEFAULT_MIN_COUNT = 2
        try:
            min_count = max(1, int(request.GET.get('min_count', DEFAULT_MIN_COUNT)))
        except (ValueError, TypeError):
            min_count = DEFAULT_MIN_COUNT

        # Step 1: ownership map {login_account_id: {user_id, username}}
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

        empty_ctx = {
            **self.admin_site.each_context(request),
            'title': 'Shared IP Report',
            'ip_groups': [],
            'flagged_count': 0,
            'min_count': min_count,
            'default_min_count': DEFAULT_MIN_COUNT,
            'changelist_url': reverse('admin:accounts_loginaccountownership_changelist'),
        }

        if not ownership_map:
            return TemplateResponse(
                request,
                'admin/accounts/loginaccountownership/shared_ip_report.html',
                empty_ctx,
            )

        # Step 2: game accounts keyed by lsaccount_id (game DB)
        # {lsaccount_id: {accid, account_name}}
        game_accounts = (
            Account.objects.using('game_database')
            .filter(lsaccount_id__in=list(ownership_map.keys()))
            .values('id', 'name', 'lsaccount_id')
        )
        # Two maps for the join in step 4
        accid_to_lsid = {}       # accid → lsaccount_id
        accid_to_name = {}       # accid → game account name
        for ga in game_accounts:
            accid_to_lsid[ga['id']] = ga['lsaccount_id']
            accid_to_name[ga['id']] = ga['name']

        if not accid_to_lsid:
            return TemplateResponse(
                request,
                'admin/accounts/loginaccountownership/shared_ip_report.html',
                empty_ctx,
            )

        # Step 3: account_ip rows for owned game accounts, filtered by min_count (game DB)
        account_ips = (
            AccountIp.objects.using('game_database')
            .filter(accid__in=list(accid_to_lsid.keys()), count__gte=min_count)
            .values('accid', 'ip', 'count', 'lastused')
        )

        # Step 4: group by IP → collect (web user, game account, count, lastused) per IP
        # {ip: {'users': {user_id: username}, 'entries': [...]}}
        ip_map = defaultdict(lambda: {'users': {}, 'entries': []})

        for row in account_ips:
            lsid = accid_to_lsid.get(row['accid'])
            if lsid is None:
                continue
            owner = ownership_map.get(lsid)
            if not owner:
                continue
            ip = (row['ip'] or '').strip()
            if not ip:
                continue
            bucket = ip_map[ip]
            bucket['users'][owner['user_id']] = owner['username']
            bucket['entries'].append({
                'accid': row['accid'],
                'account_name': accid_to_name.get(row['accid'], str(row['accid'])),
                'user_id': owner['user_id'],
                'username': owner['username'],
                'count': row['count'],
                'lastused': row['lastused'],
            })

        # Step 5: keep only IPs shared across 2+ distinct web users
        flagged_ips = {
            ip: data
            for ip, data in ip_map.items()
            if len(data['users']) >= 2
        }

        # Step 6: fetch exemptions for flagged IPs (game DB, targeted query)
        exemption_map = {}
        if flagged_ips:
            exemptions = (
                IpExemption.objects.using('game_database')
                .filter(exemption_ip__in=list(flagged_ips.keys()))
                .values('exemption_ip', 'exemption_amount')
            )
            exemption_map = {
                row['exemption_ip']: row['exemption_amount']
                for row in exemptions
            }

        # Step 7: build sorted output
        ip_groups = []
        for ip, data in flagged_ips.items():
            # Sort entries: by username then account name, then descending count
            data['entries'].sort(key=lambda e: (e['username'], e['account_name'], -e['count']))
            ip_groups.append({
                'ip': ip,
                'user_count': len(data['users']),
                'users': sorted(data['users'].values()),
                'entries': data['entries'],
                'total_connections': sum(e['count'] for e in data['entries']),
                'exemption_amount': exemption_map.get(ip),
                'is_exempt': ip in exemption_map,
            })

        # Non-exempt first, then by descending user count, then descending total connections
        ip_groups.sort(key=lambda g: (g['is_exempt'], -g['user_count'], -g['total_connections']))

        return TemplateResponse(
            request,
            'admin/accounts/loginaccountownership/shared_ip_report.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Shared IP Report',
                'ip_groups': ip_groups,
                'flagged_count': len(ip_groups),
                'min_count': min_count,
                'default_min_count': DEFAULT_MIN_COUNT,
                'changelist_url': reverse('admin:accounts_loginaccountownership_changelist'),
            },
        )

    def unlinked_report_view(self, request):
        all_ls_ids = set(
            LoginAccounts.objects.using('login_server_database')
            .values_list('id', flat=True)
        )
        linked_ids = set(
            LoginAccountOwnership.objects.values_list('login_account_id', flat=True)
        )
        unlinked_ids = all_ls_ids - linked_ids

        unlinked_accounts = []
        if unlinked_ids:
            unlinked_accounts = list(
                LoginAccounts.objects.using('login_server_database')
                .filter(id__in=unlinked_ids)
                .values('id', 'account_name', 'account_email', 'last_login_date', 'source_loginserver')
                .order_by('account_name')
            )

        return TemplateResponse(
            request,
            'admin/accounts/loginaccountownership/unlinked_report.html',
            {
                **self.admin_site.each_context(request),
                'title': 'Unlinked Login Accounts',
                'unlinked_accounts': unlinked_accounts,
                'unlinked_count': len(unlinked_accounts),
                'changelist_url': reverse('admin:accounts_loginaccountownership_changelist'),
            },
        )


admin.site.register(LoginAccountOwnership, LoginAccountOwnershipAdmin)


# ---------------------------------------------------------------------------
# IP Exemptions — game database, manual DB routing required
# ---------------------------------------------------------------------------

class IpExemptionAdmin(admin.ModelAdmin):
    list_display = ['exemption_ip', 'exemption_amount']
    search_fields = ['exemption_ip']
    ordering = ['exemption_ip']

    def get_queryset(self, request):
        return super().get_queryset(request).using('game_database')

    def save_model(self, request, obj, form, change):
        obj.save(using='game_database')

    def delete_model(self, request, obj):
        obj.delete(using='game_database')

    def delete_queryset(self, request, queryset):
        queryset.using('game_database').delete()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Fetch the box-limit rules from the game DB
        box_rules = list(
            RuleValues.objects.using('game_database')
            .filter(rule_name__icontains='AccountSessionLimit')
            .values('rule_name', 'rule_value', 'notes')
        )
        extra_context['box_rules'] = box_rules
        # Derive the effective limit: first matching rule value, else compiled default of 1
        extra_context['effective_limit'] = box_rules[0]['rule_value'] if box_rules else '1'
        extra_context['limit_is_default'] = not bool(box_rules)

        # Inline IP lookup
        ip_q = request.GET.get('ip_q', '').strip()
        extra_context['ip_q'] = ip_q
        if ip_q:
            matches = list(
                LoginAccounts.objects.using('login_server_database')
                .filter(account_name__icontains=ip_q)
                .values('account_name', 'last_ip_address', 'last_login_date')
                .order_by('account_name')[:20]
            )
            # Flag which IPs already have an exemption
            ips_with_exemption = set(
                IpExemption.objects.using('game_database')
                .filter(exemption_ip__in=[m['last_ip_address'] for m in matches if m['last_ip_address']])
                .values_list('exemption_ip', flat=True)
            )
            for m in matches:
                m['has_exemption'] = m['last_ip_address'] in ips_with_exemption
            extra_context['ip_lookup_results'] = matches
        else:
            extra_context['ip_lookup_results'] = None

        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(IpExemption, IpExemptionAdmin)


