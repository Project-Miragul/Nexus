from accounts.models import Account, LoginAccounts
from accounts.utils import get_owned_login_account_ids
from common.models.characters import Characters


def valid_character_ownership(user_or_username, character_id: str) -> bool:
    """
    Returns True if the given user owns the character with the given character_id.
    Accepts a User instance or a username string.
    """
    target_character = Characters.objects.filter(id=character_id).first()
    if target_character is None:
        return False

    owned_ids = get_owned_login_account_ids(user_or_username)
    for account_name in LoginAccounts.objects.filter(id__in=owned_ids).values('account_name'):
        game_account = Account.objects.filter(name=account_name['account_name']).first()
        if game_account is None:
            continue
        if Characters.objects.filter(account_id=game_account.id, id=target_character.id).exists():
            return True
    return False
