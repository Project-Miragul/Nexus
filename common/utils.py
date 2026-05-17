import math
from accounts.models import Account, LoginAccounts
from accounts.utils import get_owned_login_account_ids


def valid_game_account_owner(user_or_username, game_account_id: str) -> bool:
    """
    Returns True if the given user owns the game account.
    Accepts a User instance or a username string.
    """
    game_account = Account.objects.filter(id=game_account_id).first()
    if game_account is None:
        return False

    owned_ids = list(get_owned_login_account_ids(user_or_username))
    owned_account_names = [
        a['account_name'].lower()
        for a in LoginAccounts.objects.filter(id__in=owned_ids).values('account_name')
    ]
    return game_account.name.lower() in owned_account_names


def calculate_item_price(item_price: int):
    """
    Takes the item price in copper and returns the price in platinum, gold, silver, and copper

    :param item_price: an integer value in units of copper
    :return: a list of platinum, gold, silver, and copper
    """
    platinum = math.floor(item_price / 1000),
    gold = math.floor((item_price % 1000) / 100),
    silver = math.floor((item_price % 100) / 10),
    copper = item_price % 10

    return platinum, gold, silver, copper
