"""
utils.py - reusable utility functions used in character views
"""
from collections import namedtuple

from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from django.db.models import F

from accounts.models import Account
from accounts.utils import get_owned_login_account_ids
from characters.templatetags.data_utilities import player_skill, spell_target_type
from common.faction import FactionMods
from common.models.characters import CharacterSkills
from common.models.characters import CharacterSpells
from common.models.faction import FactionListMod
from common.models.guilds import Guilds
from common.models.guilds import GuildMembers
from common.models.spells import SpellsNew
from spells.models import SpellExpansion, SpellScroll


def get_character_inventory(character_id: int) -> tuple:
    cursor = connections['game_database'].cursor()
    cursor.execute("""SELECT ci.item_id, i.name, i.icon, ci.slot_id, ci.charges, i.maxcharges, i.stackable, i.stacksize
                      FROM inventory ci LEFT OUTER JOIN items i ON ci.item_id = i.id
                      WHERE ci.character_id = %s
                      ORDER BY ci.slot_id""", [character_id])
    character_inventory = cursor.fetchall()
    return character_inventory


def get_character_keyring(character_id: int) -> tuple:
    cursor = connections['game_database'].cursor()
    cursor.execute(
        """SELECT ck.item_id, i.Name
           FROM keyring as ck LEFT OUTER JOIN items as i ON ck.item_id = i.id
           WHERE ck.char_id = '%s'
           ORDER BY i.Name;""", [character_id])
    character_keyring = cursor.fetchall()
    return character_keyring


def get_faction_information(character_id: int, race_id: int, class_id: int, deity_id: int) -> list:
    cursor = connections['game_database'].cursor()
    cursor.execute(
        """SELECT fl.id, fl.name, fl.base, cfv.current_value
           FROM faction_values as cfv LEFT OUTER JOIN faction_list as fl ON fl.id = cfv.faction_id
           WHERE cfv.char_id = '%s'
           ORDER BY fl.name;
        """, [character_id])
    character_faction_list = cursor.fetchall()
    final_faction = []
    race_mod_name = ''.join(['r', str(race_id)])
    class_mod_name = ''.join(['c', str(class_id)])
    deity_mod_name = ''.join(['d', str(deity_id)])
    FactionTableRow = namedtuple("FactionTableRow", "id name base current_value")
    for faction in character_faction_list:
        faction_table_row = FactionTableRow(faction[0], faction[1], faction[2], faction[3])
        faction_modifiers = FactionListMod.objects.filter(faction_id=faction_table_row.id)
        fm = FactionMods()
        fm.base_mod = faction_table_row.base
        fm.race_mod = 0
        fm.class_mod = 0
        fm.deity_mod = 0
        for modifier in faction_modifiers:
            if race_mod_name == modifier.mod_name:
                fm.race_mod = modifier.mod
            if class_mod_name == modifier.mod_name:
                fm.class_mod = modifier.mod
            if deity_mod_name == modifier.mod_name:
                fm.deity_mod = modifier.mod
        modifiers = fm.base_mod + fm.race_mod + fm.class_mod + fm.deity_mod
        row = faction[0], faction[1], modifiers, faction[3]
        if len(row) == 4:
            final_faction.append(row)

    return final_faction


def get_guild_information(character_id: int):
    member = GuildMembers.objects.filter(char_id=character_id).first()
    if member is None:
        return None, None
    guild = member.guild_id
    guild_members = GuildMembers.objects.filter(guild_id=guild.id)
    return guild, guild_members


def get_skill_information(character_id: int):
    character_skills_unfiltered = CharacterSkills.objects.filter(id=character_id)
    character_magic_songs = []
    character_skills = []
    for skill in character_skills_unfiltered:
        if skill.skill_id in [4, 5, 12, 13, 14, 18, 24, 31, 41, 43, 44, 45, 46, 47, 49, 54, 70]:
            character_magic_songs.append(skill)
        else:
            character_skills.append(skill)
    return character_magic_songs, character_skills


def get_spell_information(character_id: int, class_id: int):
    scribed_spells = CharacterSpells.objects.filter(id=character_id)
    character_spells = []
    for spell in scribed_spells:
        try:
            character_spells.append(spell.spell_id.id)
        except ObjectDoesNotExist:
            continue

    class_level_field = f'classes{class_id}'
    spell_qs = (
        SpellsNew.objects
        .filter(**{f'{class_level_field}__gte': 1, f'{class_level_field}__lte': 65})
        .annotate(level=F(class_level_field))
        .order_by(class_level_field, 'name')
    )

    expansion_map = {se.id: se.expansion for se in SpellExpansion.objects.all()}

    spell_ids = list(spell_qs.values_list('id', flat=True))
    scroll_map = {
        ss.spell_id: (ss.scroll_item_id, ss.scroll_item_name)
        for ss in SpellScroll.objects.filter(spell_id__in=spell_ids)
    }

    spell_list = {}
    for spell in spell_qs:
        level = spell.level
        spell_data = {
            'name': spell.name,
            'spell_id': spell.id,
            'level': level,
            'expansion': expansion_map.get(spell.id, 0),
            'custom_icon': spell.custom_icon,
            'classes1': spell.classes1,
            'classes2': spell.classes2,
            'classes3': spell.classes3,
            'classes4': spell.classes4,
            'classes5': spell.classes5,
            'classes6': spell.classes6,
            'classes7': spell.classes7,
            'classes8': spell.classes8,
            'classes9': spell.classes9,
            'classes10': spell.classes10,
            'classes11': spell.classes11,
            'classes12': spell.classes12,
            'classes13': spell.classes13,
            'classes14': spell.classes14,
            'classes15': spell.classes15,
            'mana': spell.mana,
            'skill': player_skill(spell.skill),
            'target_type': spell_target_type(spell.target_type),
            'scrolls': [scroll_map[spell.id]] if spell.id in scroll_map else [],
        }
        if level in spell_list:
            spell_list[level].append(spell_data)
        else:
            spell_list[level] = [spell_data]

    return character_spells, spell_list


def get_owned_characters(user_or_username):
    owned_ids = get_owned_login_account_ids(user_or_username)
    game_accounts = [Account.objects.filter(lsaccount_id=ls_id) for ls_id in owned_ids]
    characters = {}
    accounts = []
    for account in game_accounts:
        try:
            accounts.append(account.values('id', 'name', 'time_creation')[0])
            game_account_id = account.values('id')[0]['id']
        except IndexError:
            continue
        if game_account_id is not None:
            cursor = connections['game_database'].cursor()
            cursor.execute(
                """SELECT cd.id, cd.name, cd.class, cd.race, cd.level, cd.zone_id,
                          cd.x, cd.y, cd.z, a.id, a.Name, a.time_creation
                   FROM character_data as cd LEFT OUTER JOIN account as a ON cd.account_id = a.id 
                   WHERE cd.account_id  = '%s' 
                   ORDER BY cd.name;""", [game_account_id])
            results = cursor.fetchall()

            Character = namedtuple("Character",
                                   "char_id char_name char_class char_race char_level zone_id x y z"
                                   " account_id account_name")
            for result in results:
                temp = Character(result[0], result[1], result[2], result[3],
                                 result[4], result[5], result[6], result[7],
                                 result[8], result[9], result[10])
                if temp.account_name not in characters:
                    characters[temp.account_name] = dict()
                    characters[temp.account_name]['time_creation'] = result[11]
                    characters[temp.account_name]['characters'] = dict()
                characters[temp.account_name]['characters'][temp.char_name] = temp

    return characters

def get_exp_for_level(check_level, race_id):
    base = check_level * check_level * check_level
    playermod = 10
    mod = 0.0

    match race_id:
        case 1024: # Halfing
            playermod *= 95.0
        case 1|4|8|16|32|64|128|2048|8192:
            playermod *= 100.0
        case 2: # Barb
            playermod *= 105.0
        case 512: # Ogre
            playermod *= 115.0
        case 256|4096: # Troll/Iksar
            playermod *= 120.0
        case _:
            playermod *= 100.0
    if check_level <= 29:
        mod = 1.0
    elif check_level <= 34:
        mod = 1.1
    elif check_level <= 39:
        mod = 1.2
    elif check_level <= 44:
        mod = 1.3
    elif check_level <= 50:
        mod = 1.4
    elif check_level == 51:
        mod = 1.5
    elif check_level == 52:
        mod = 1.6
    elif check_level == 53:
        mod = 1.7
    elif check_level == 54:
        mod = 1.9
    elif check_level == 55:
        mod = 2.1
    elif check_level == 56:
        mod = 2.3
    elif check_level == 57:
        mod = 2.5
    elif check_level == 58:
        mod = 2.7
    elif check_level == 59:
        mod = 3.0
    elif check_level == 60:
        mod = 3.1
    elif check_level == 61:
        mod = 3.3
    elif check_level == 62:
        mod = 3.5
    elif check_level == 63:
        mod = 3.7
    elif check_level == 64:
        mod = 3.9
    else:
        mod = 4.1

    final_xp = base * playermod * mod

    return int(final_xp)

def get_consider_levels(level):
    green_high = 0
    light_blue_high = 0

    if level <= 7:
        green_high = -4
    elif level <= 8:
        green_high = -5
        light_blue_high = -4
    elif level <= 12:
        green_high = -6
        light_blue_high = -4
    elif level <= 16:
        green_high = -7
        light_blue_high = -5
    elif level <= 20:
        green_high = -8
        light_blue_high = -6
    elif level <= 24:
        green_high = -9
        light_blue_high = -7
    elif level <= 28:
        green_high = -10
        light_blue_high = -8
    elif level <= 30:
        green_high = -11
        light_blue_high = -9
    elif level <= 32:
        green_high = -12
        light_blue_high = -9
    elif level <= 36:
        green_high = -13
        light_blue_high = -10
    elif level <= 40:
        green_high = -14
        light_blue_high = -11
    elif level <= 44:
        green_high = -16
        light_blue_high = -12
    elif level <= 48:
        green_high = -17
        light_blue_high = -13
    elif level <= 52:
        green_high = -18
        light_blue_high = -14
    elif level <= 54:
        green_high = -19
        light_blue_high = -15
    elif level <= 56:
        green_high = -20
        light_blue_high = -15
    elif level <= 60:
        green_high = -21
        light_blue_high = -16
    elif level <= 61:
        green_high = -19
        light_blue_high = -14
    elif level <= 62:
        green_high = -17
        light_blue_high = -12
    else:
        green_high = -16
        light_blue_high = -11

    con = {
        'green': {
            'min': 0 if level <= 4 else 1,
            'max': 0 if level <= 4 else level + green_high},
        'lightblue': {'min': 0, 'max': 0},
        'blue': {'min': 0, 'max': 0},
        'white': level,
        'yellow': {'min': level + 1, 'max': level + 2},
        'red': {'min': level + 3, 'max': 68},
    }

    if level == 1:
        return con

    if level <= 4:
        con['blue']['min'] = 1
        con['blue']['max'] = level - 1
        return con

    con['green']['min'] = 1
    con['green']['max'] = level + green_high

    con['blue']['max'] = level - 1
    if light_blue_high == 0:
        con['blue']['min'] = con['green']['max'] + 1
        return con

    con['lightblue']['min'] = con['green']['max'] + 1
    con['lightblue']['max'] = level + light_blue_high
    con['blue']['min'] = con['lightblue']['max'] + 1

    return con

def rule_of_six(caster_level):
    """Rule of six level is the level mobs will, without any doubt, resist your spells.
    It's actually 7 levels at the start, but the six meant the number of levels you could still hit them.
    The spectrum gets a little wider later on is why I put them there"""
    npc_level1 = caster_level + 7
    npc_level2 = int(caster_level * 1.25)
    npc_level = max(npc_level1, npc_level2)

    return npc_level
