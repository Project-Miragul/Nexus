from django import template
from django.contrib.auth.models import User
from django.utils import timezone

register = template.Library()


@register.simple_tag
def nexus_dashboard_counts():
    from accounts.models import Account, LoginAccounts, LoginAccountOwnership

    counts = {
        'suspended': 0,
        'banned': 0,
        'unlinked': 0,
        'new_today': 0,
        'web_users': 0,
    }
    try:
        now = timezone.now()
        counts['suspended'] = (
            Account.objects.using('game_database')
            .filter(suspendeduntil__gt=now)
            .count()
        )
        counts['banned'] = (
            Account.objects.using('game_database')
            .filter(revoked=1)
            .count()
        )
        all_ls_ids = set(
            LoginAccounts.objects.using('login_server_database')
            .values_list('id', flat=True)
        )
        linked_ids = set(
            LoginAccountOwnership.objects.values_list('login_account_id', flat=True)
        )
        counts['unlinked'] = len(all_ls_ids - linked_ids)
        counts['new_today'] = User.objects.filter(date_joined__date=now.date()).count()
        counts['web_users'] = User.objects.count()
    except Exception:
        pass

    return counts
