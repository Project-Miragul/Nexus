import datetime
import json
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connections

from common.models.characters import Characters
from common.models.characters import CharacterCurrency
from common.models.characters import CharacterLanguages
from django.db.models import Q
from common.models.guilds import GuildMembers, GuildRanks, GuildRelations
from common.models.guilds import Guilds
from common.models.zones import Zone
from common.models.items import DiscoveredItems
from common.utils import valid_game_account_owner
from common.constants import PLAYER_RACIAL_EXP_MODIFIERS

from accounts.models import Account, AccountMetadata

from characters.utils import get_character_keyring
from characters.utils import get_character_inventory
from characters.utils import get_faction_information
from characters.utils import get_guild_information
from characters.utils import get_skill_information
from characters.utils import get_spell_information
from characters.utils import get_owned_characters
from characters.utils import get_exp_for_level
from characters.utils import get_consider_levels
from characters.utils import rule_of_six


def index_request(request):
    if request.method == "GET":
        return render(request=request, template_name="characters/index.html")
    return redirect("accounts:login")


# Zone flag ID → checkbox IDs to pre-check.
# Each entry represents: "having zone access to X means these quest steps are complete."
_ZONE_FLAG_CHECKBOXES = {
    # Crypt of Decay — requires completing the Grummus/Fuirstel chain
    200: ['grummus1', 'grummus2', 'grummus3', 'grummus4'],
    # Plane of Torment — requires Bertoxxulous + Terris done, then Fahlia Shadyglade pre-flag
    207: ['grummus4', 'bert4', 'terris5', 'saryrn1'],
    # Plane of Valor — requires PoJ trial
    208: ['poj1', 'poj2', 'poj3'],
    # Plane of Storms — requires PoJ trial to enter
    210: ['poj1', 'poj2', 'poj3', 'pos1'],
    # Bastion of Thunder — requires Askr quest in PoStorms
    209: ['poj1', 'poj2', 'poj3', 'pos1', 'pos2'],
    # Halls of Honor — requires killing Aerin'Dar
    211: ['poj1', 'poj2', 'poj3', 'aerin1', 'aerin2'],
    # Temple of Marr — requires all 3 HoH trials
    220: ['poj1', 'poj2', 'poj3', 'aerin1', 'aerin2', 'hoh1', 'hoh2', 'hoh3', 'hoh4', 'marr1'],
    # Plane of Nightmare B (Terris Thule) — requires Hedge event complete
    221: ['terris1', 'terris2'],
    # Plane of Tactics — requires Manaetic Behemoth
    214: ['poi1', 'poi2'],
    # Tower of Solusek Ro — requires all Tier 1-3 content + Combined 2 flag
    212: [
        'poj1', 'poj2', 'poj3',
        'grummus1', 'grummus2', 'grummus3', 'grummus4',
        'terris1', 'terris2', 'terris3', 'terris4', 'terris5',
        'poi2',
        'aerin1', 'aerin2',
        'bert1', 'bert2', 'bert3', 'bert4',
        'saryrn1', 'saryrn2', 'saryrn3', 'saryrn4', 'saryrn5', 'saryrn6',
        'pos1', 'pos2',
        'bot1', 'bot2', 'bot3',
        'vallon1', 'vallon2', 'tallon1', 'tallon2', 'rztw1',
        'hoh1', 'hoh2', 'hoh3', 'hoh4',
        'marr1', 'marr2', 'marr3', 'marr4',
        'combined2', 'tosr_pre',
    ],
    # Elemental Planes (Earth, Air, Water, Earth B) — requires Tier 3 Combined flag
    215: ['combined1', 'combined3', 'elem1'],
    216: ['combined1', 'combined3', 'elem1'],
    218: ['combined1', 'combined3', 'elem1'],
    222: ['combined1', 'combined3', 'elem1'],
    # Plane of Fire — requires Solusek Ro + fire flagging
    217: ['combined1', 'combined3', 'elem1', 'tosr_solro', 'elem2'],
    # Plane of Time
    223: ['potime'],
}


def pop_flags(request):
    pre_checked = []
    loaded_character = None
    owned_character_names = []

    if request.user.is_authenticated:
        owned_chars = get_owned_characters(request.user.username)
        for account_data in owned_chars.values():
            owned_character_names.extend(account_data['characters'].keys())
        owned_character_names.sort()

        character_name = request.GET.get('character')
        if character_name:
            character = Characters.objects.filter(name=character_name).first()
            if character:
                account = Account.objects.filter(id=character.account_id).first()
                if account and valid_game_account_owner(request.user.username, str(account.id)):
                    with connections['game_database'].cursor() as cur:
                        cur.execute(
                            "SELECT DISTINCT zoneID FROM zone_flags WHERE charID = %s",
                            [character.id],
                        )
                        zone_ids = {row[0] for row in cur.fetchall()}
                    checked = set()
                    for zid in zone_ids:
                        checked.update(_ZONE_FLAG_CHECKBOXES.get(zid, []))
                    pre_checked = sorted(checked)
                    loaded_character = character_name

    return render(request=request, template_name="characters/pop_flags.html", context={
        'pre_checked': json.dumps(pre_checked),
        'loaded_character': loaded_character,
        'owned_character_names': owned_character_names,
    })


def experience(request, race_id=None):
    if race_id is not None:
        cursor = connections['game_database'].cursor()
        cursor.execute("""SELECT level, exp_mod, aa_exp_mod FROM level_exp_mods""")
        exp_mod = cursor.fetchall()
        level_data = []
        prev_xp =  0

        for level in range(1, 66): # levels 1 through 65 (non-inclusive of last value)
            current_xp = get_exp_for_level(level, race_id)
            difference = current_xp - prev_xp
            consider_levels = get_consider_levels(level)
            six_rule = rule_of_six(level)
            level_data.append({
                'level': level,
                'experience': current_xp,
                'difference': difference,
                'con_levels': consider_levels,
                'exp_mod': exp_mod[level-1][1],
                'six_rule': six_rule
            })
            prev_xp = current_xp
        selected_race, racial_modifier = PLAYER_RACIAL_EXP_MODIFIERS.get(race_id, 0)

        return render(request=request, template_name="characters/exp.html",
                      context={"PLAYER_RACIAL_EXP_MODIFIERS": PLAYER_RACIAL_EXP_MODIFIERS,
                               "level_data": level_data,
                               "selected_race": selected_race,
                               "racial_modifier": racial_modifier,
                               "race": race_id})
    else:
        return render(request=request, template_name="characters/exp.html",
                      context={"PLAYER_RACIAL_EXP_MODIFIERS": PLAYER_RACIAL_EXP_MODIFIERS,})

@login_required
def list_characters(request, game_account_name):
    """
    Defines view for https://url.tld/characters/list/<str:game_account_name>

    :param request:
    :param game_account_name:
    :return:
    """
    if request.method == "GET":

        forum_name = request.user.username
        game_account = Account.objects.using('game_database').filter(name__iexact=game_account_name).first()
        if game_account is None:
            messages.error(request, "The world server has not seen this account. If this account is new, "
                                    "please log in to character select first.")
            return redirect("accounts:list_accounts")
        if not valid_game_account_owner(forum_name, str(game_account.id)):
            raise Http404("Either this account does not exist or does not belong to you.  If you have registered this "
                          "account with the login server, you must log in to the game server at least once before "
                          "attempting to view this page.")

        if game_account.id is not None:
            is_mule = AccountMetadata.objects.filter(
                login_account_id=game_account.lsaccount_id, is_trader=True
            ).exists()
            characters = Characters.objects.using('game_database').filter(account_id=game_account.id)
            return render(request=request, template_name="characters/list.html",
                          context={"characters": characters,
                                   "is_mule": is_mule,
                                   "game_account_name": game_account.name, }
                          )
    return redirect("accounts:login")


@login_required
def view_character(request, character_name):
    """
    Defines view for https://url.tld/characters/view/<str:character_name>

    :param request:
    :param character_name:
    :return:
    """
    if request.method == "GET":

        character = Characters.objects.filter(name=character_name).first()
        if character is None:
            raise Http404("This character does not exist")

        account = Account.objects.filter(id=character.account_id).first()

        forum_name = request.user.username
        if not valid_game_account_owner(forum_name, str(account.id)):
            raise Http404("This account does not exist")

        character_currency = CharacterCurrency.objects.filter(id=character.id).first()

        character_magic_songs, character_skills = get_skill_information(character_id=character.id)

        character_keyring = get_character_keyring(character_id=character.id)

        character_languages = CharacterLanguages.objects.filter(id=character.id)

        character_faction_values = get_faction_information(character_id=character.id,
                                                           race_id=character.race,
                                                           class_id=character.class_name,
                                                           deity_id=character.deity)

        character_spells, spell_list = get_spell_information(character_id=character.id,
                                                             class_id=character.class_name)

        discovered_items = DiscoveredItems.objects.filter(char_name=character.name)

        # 0 - Unknown, 1 - Warrior, 7 - Monk, 9 - Rogue
        non_casters = [0, 1, 7, 9]

        guild, guild_members = get_guild_information(character_id=character.id)

        guild_rank_titles = {
            0: "Member", 1: "Officer", 2: "Leader",
            3: "Rank 3", 4: "Rank 4", 5: "Rank 5",
            6: "Rank 6", 7: "Rank 7", 8: "Rank 8",
        }
        guild_zone_map = {}
        guild_leader_name = None
        guild_relations = []
        if guild is not None:
            for gr in GuildRanks.objects.filter(guild_id=guild.id):
                if gr.title:
                    guild_rank_titles[gr.rank] = gr.title
            zone_ids = set(guild_members.values_list('char_id__zone_id', flat=True))
            guild_zone_map = {
                z.zone_id_number: z.long_name
                for z in Zone.objects.filter(zone_id_number__in=zone_ids)
            }
            guild_leader_name = Characters.objects.filter(id=guild.leader).values_list('name', flat=True).first()
            guild_members = guild_members.order_by('-rank', '-char_id__level')

            relation_rows = GuildRelations.objects.filter(Q(guild1=guild.id) | Q(guild2=guild.id))
            other_guild_ids = [r.guild2 if r.guild1 == guild.id else r.guild1 for r in relation_rows]
            other_guilds = {g.id: g.name for g in Guilds.objects.filter(id__in=other_guild_ids)}
            guild_relations = [
                {
                    'guild_name': other_guilds.get(r.guild2 if r.guild1 == guild.id else r.guild1, 'Unknown'),
                    'relation': r.relation,
                }
                for r in relation_rows
            ]

        character_inventory = get_character_inventory(character_id=character.id)

        character_list = get_owned_characters(request.user.username)

        last_login = datetime.datetime.fromtimestamp(character.last_login)
        birthday = datetime.datetime.fromtimestamp(character.birthday)
        time_played = datetime.timedelta(seconds=character.time_played)
        face_image = ''.join(["race_", str(character.race), "_gender_",
                              str(character.gender), "_face_", str(character.face), ".png"])

        return render(request=request, template_name="characters/view.html",
                      context={
                          "account": account,
                          "birthday": birthday,
                          "character": character,
                          "character_currency": character_currency,
                          "character_faction_values": character_faction_values,
                          "character_inventory": character_inventory,
                          "character_keyring": character_keyring,
                          "character_languages": character_languages,
                          "character_list": character_list,
                          "character_magic_songs": character_magic_songs,
                          "character_skills": character_skills,
                          "character_spells": character_spells,
                          "discovered_items": discovered_items,
                          "face_image": face_image,
                          "guild": guild,
                          "guild_leader_name": guild_leader_name,
                          "guild_members": guild_members,
                          "guild_rank_titles": guild_rank_titles,
                          "guild_relations": guild_relations,
                          "guild_zone_map": guild_zone_map,
                          "user_is_guild_leader": guild is not None and character.id == guild.leader,
                          "last_login": last_login,
                          "non_casters": non_casters,
                          "time_played": time_played,
                          "spell_list": spell_list,
                      }
                      )

    return redirect("accounts:login")


@login_required
def promote_member(request, char_id):
    if request.method != 'POST':
        return redirect('characters:index')

    try:
        new_rank = int(request.POST.get('new_rank', -1))
        if new_rank not in range(9):
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Invalid rank value.")
        return redirect('characters:index')

    member = GuildMembers.objects.filter(char_id=char_id).first()
    if member is None:
        raise Http404

    guild = member.guild_id
    leader_char = Characters.objects.filter(id=guild.leader).first()
    if leader_char is None:
        raise Http404

    leader_account = Account.objects.filter(id=leader_char.account_id).first()
    if leader_account is None or not valid_game_account_owner(request.user.username, str(leader_account.id)):
        raise Http404

    member.rank = new_rank
    member.save()

    messages.success(request, "Rank updated.")
    referer = request.META.get('HTTP_REFERER', '/characters/')
    return redirect(referer)
