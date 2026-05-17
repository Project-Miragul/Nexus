from django.db import models
from django.db.models import SmallIntegerField
from common.models.spells import SpellsNew


class Characters(models.Model):
    """
    This model maps to the character_data table in the database.
    """

    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(default=0, null=False)
    name = models.CharField(max_length=64, default='', unique=True, null=False, blank=True)
    last_name = models.CharField(max_length=64, default='', null=False, blank=True)
    title = models.CharField(max_length=32, default='', null=False, blank=True)
    suffix = models.CharField(max_length=32, default='', null=False, blank=True)
    zone_id = models.IntegerField(default=0, null=False)
    zone_instance = models.IntegerField(default=0, null=False)
    y = models.FloatField(default=0, null=False)
    x = models.FloatField(default=0, null=False)
    z = models.FloatField(default=0, null=False)
    heading = models.FloatField(default=0, null=False)
    gender = models.SmallIntegerField(default=0, null=False)
    race = models.SmallIntegerField(default=0, null=False)
    class_name = models.SmallIntegerField(default=0, null=False, db_column="`class`")
    level = models.IntegerField(default=0, null=False)
    deity = models.IntegerField(default=0, null=False)
    birthday = models.IntegerField(default=0, null=False)
    last_login = models.IntegerField(default=0, null=False)
    time_played = models.IntegerField(default=0, null=False)
    level2 = models.SmallIntegerField(default=0, null=False)
    anon = models.SmallIntegerField(default=0, null=False)
    gm = models.SmallIntegerField(default=0, null=False)
    face = models.IntegerField(default=0, null=False)
    hair_color = models.SmallIntegerField(default=0, null=False)
    hair_style = models.SmallIntegerField(default=0, null=False)
    beard = models.SmallIntegerField(default=0, null=False)
    beard_color = models.SmallIntegerField(default=0, null=False)
    eye_color_1 = models.SmallIntegerField(default=0, null=False)
    eye_color_2 = models.SmallIntegerField(default=0, null=False)
    drakkin_heritage = models.IntegerField(default=0, null=False)
    drakkin_tattoo = models.IntegerField(default=0, null=False)
    drakkin_details = models.IntegerField(default=0, null=False)
    ability_time_seconds = models.SmallIntegerField(default=0, null=False)
    ability_number = models.SmallIntegerField(default=0, null=False)
    ability_time_minutes = models.SmallIntegerField(default=0, null=False)
    ability_time_hours = models.SmallIntegerField(default=0, null=False)
    exp = models.IntegerField(default=0, null=False)
    exp_enabled = models.SmallIntegerField(default=1, null=False)
    aa_points_spent = models.IntegerField(default=0, null=False)
    aa_exp = models.IntegerField(default=0, null=False)
    aa_points = models.IntegerField(default=0, null=False)
    group_leadership_exp = models.IntegerField(default=0, null=False)
    raid_leadership_exp = models.IntegerField(default=0, null=False)
    group_leadership_points = models.IntegerField(default=0, null=False)
    raid_leadership_points = models.IntegerField(default=0, null=False)
    points = models.IntegerField(default=0, null=False)
    cur_hp = models.IntegerField(default=0, null=False)
    mana = models.IntegerField(default=0, null=False)
    endurance = models.IntegerField(default=0, null=False)
    intoxication = models.IntegerField(default=0, null=False)
    str = models.IntegerField(default=0, null=False)
    sta = models.IntegerField(default=0, null=False)
    cha = models.IntegerField(default=0, null=False)
    dex = models.IntegerField(default=0, null=False)
    int_stat = models.IntegerField(default=0, null=False, db_column='`int`')
    agi = models.IntegerField(default=0, null=False)
    wis = models.IntegerField(default=0, null=False)
    extra_haste = models.IntegerField(default=0, null=False)
    zone_change_count = models.IntegerField(default=0, null=False)
    toxicity = models.IntegerField(default=0, null=False)
    hunger_level = models.IntegerField(default=0, null=False)
    thirst_level = models.IntegerField(default=0, null=False)
    ability_up = models.IntegerField(default=0, null=False)
    ldon_points_guk = models.IntegerField(default=0, null=False)
    ldon_points_mir = models.IntegerField(default=0, null=False)
    ldon_points_mmc = models.IntegerField(default=0, null=False)
    ldon_points_ruj = models.IntegerField(default=0, null=False)
    ldon_points_tak = models.IntegerField(default=0, null=False)
    ldon_points_available = models.IntegerField(default=0, null=False)
    tribute_time_remaining = models.IntegerField(default=0, null=False)
    career_tribute_points = models.IntegerField(default=0, null=False)
    tribute_points = models.IntegerField(default=0, null=False)
    tribute_active = models.IntegerField(default=0, null=False)
    pvp_status = models.SmallIntegerField(default=0, null=False)
    pvp_kills = models.IntegerField(default=0, null=False)
    pvp_deaths = models.IntegerField(default=0, null=False)
    pvp_current_points = models.IntegerField(default=0, null=False)
    pvp_career_points = models.IntegerField(default=0, null=False)
    pvp_best_kill_streak = models.IntegerField(default=0, null=False)
    pvp_worst_death_streak = models.IntegerField(default=0, null=False)
    pvp_current_kill_streak = models.IntegerField(default=0, null=False)
    pvp2 = models.IntegerField(default=0, null=False)
    pvp_type = models.IntegerField(default=0, null=False)
    show_helm = models.IntegerField(default=0, null=False)
    group_auto_consent = models.SmallIntegerField(default=0, null=False)
    raid_auto_consent = models.SmallIntegerField(default=0, null=False)
    guild_auto_consent = models.SmallIntegerField(default=0, null=False)
    leadership_exp_on = models.SmallIntegerField(default=0, null=False)
    rest_timer = models.IntegerField(default=0, null=False, db_column='RestTimer')
    air_remaining = models.IntegerField(default=0, null=False)
    autosplit_enabled = models.IntegerField(default=0, null=False)
    lfp = models.SmallIntegerField(default=0, null=False)
    lfg = models.SmallIntegerField(default=0, null=False)
    mailkey = models.CharField(max_length=16, default='', null=False)
    xtargets = models.SmallIntegerField(default=5, null=False)
    first_login = models.IntegerField(default=0, null=False)
    ingame = models.SmallIntegerField(default=0, null=False)
    e_aa_effects = models.IntegerField(default=0, null=False)
    e_percent_to_aa = models.IntegerField(default=0, null=False)
    e_expended_aa_spent = models.IntegerField(default=0, null=False)
    aa_points_spent_old = models.IntegerField(default=0, null=False)
    aa_points_old = models.IntegerField(default=0, null=False)
    e_last_invsnapshot = models.IntegerField(default=0, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    illusion_block = models.SmallIntegerField(default=0, null=False)

    class Meta:
        db_table = "character_data"
        verbose_name_plural = 'Characters'
        managed = False

class CharacterAlternateAbility(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    aa_id = models.PositiveSmallIntegerField(default=0)
    aa_value = models.PositiveSmallIntegerField(default=0)
    charges = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'character_alternate_abilities'
        verbose_name_plural = 'Character Alternate Abilities'
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['id', 'aa_id'], name='unique_id_aa_id')
        ]

    def __str__(self):
        return f"Character {self.id} - AA {self.aa_id}"


class CharacterCurrency(models.Model):
    """
    This model maps to the character_currency table in the database.
    """

    def __str__(self):
        return self.id

    id = models.IntegerField(primary_key=True, null=False, default=0)
    platinum = models.IntegerField(null=False, default=0)
    gold = models.IntegerField(null=False, default=0)
    silver = models.IntegerField(null=False, default=0)
    copper = models.IntegerField(null=False, default=0)
    platinum_bank = models.IntegerField(null=False, default=0)
    gold_bank = models.IntegerField(null=False, default=0)
    silver_bank = models.IntegerField(null=False, default=0)
    copper_bank = models.IntegerField(null=False, default=0)
    platinum_cursor = models.IntegerField(null=False, default=0)
    gold_cursor = models.IntegerField(null=False, default=0)
    silver_cursor = models.IntegerField(null=False, default=0)
    copper_cursor = models.IntegerField(null=False, default=0)
    radiant_crystals = models.PositiveIntegerField(null=False, default=0)
    career_radiant_crystals = models.PositiveIntegerField(null=False, default=0)
    ebon_crystals = models.PositiveIntegerField(null=False, default=0)
    career_ebon_crystals = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        db_table = 'character_currency'
        managed = False


class CharacterFactionValues(models.Model):
    """
    This model maps to the faction_values table in the database.
    """

    def __str__(self):
        return str(self.faction_id)

    char_id = models.IntegerField(primary_key=True, null=False, default=None)
    faction_id = models.IntegerField(null=False, default=None)
    current_value = SmallIntegerField(null=False, default=0)
    temp = SmallIntegerField(null=False, default=0)

    class Meta:
        db_table = "faction_values"
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['char_id', 'faction_id'], name='unique_char_faction')
        ]


class CharacterInventory(models.Model):
    """
    This model maps to the inventory table in the database.
    """

    def __str__(self):
        return str(self.item_id)

    character_id = models.IntegerField(primary_key=True, null=False, default=None)
    slot_id = models.IntegerField(null=False, default=None)
    item_id = models.IntegerField(null=True, default=0)
    charges = models.SmallIntegerField(null=True, default=0)
    color = models.PositiveIntegerField(null=False, default=0)
    augment_one = models.PositiveIntegerField(null=False, default=0)
    augment_two = models.PositiveIntegerField(null=False, default=0)
    augment_three = models.PositiveIntegerField(null=False, default=0)
    augment_four = models.PositiveIntegerField(null=False, default=0)
    augment_five = models.PositiveIntegerField(null=False, default=0)
    augment_six = models.PositiveIntegerField(null=False, default=0)
    instnodrop = models.SmallIntegerField(null=False, default=0)
    custom_data = models.TextField(null=True, default="")
    ornament_icon = models.PositiveIntegerField(null=False, default=0)
    ornament_idfile = models.PositiveIntegerField(null=False, default=0)
    ornament_hero_model = models.IntegerField(null=False, default=0)
    guid = models.BigIntegerField(null=False, default=0)

    class Meta:
        db_table = "inventory"
        managed = False


class CharacterKeyring(models.Model):
    """
    This model maps to the keyring table in the database
    """
    def __str__(self):
        return str(self.item_id)

    id = models.AutoField(primary_key=True)
    char_id = models.IntegerField(null=False, default=0)
    item_id = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'keyring'
        managed = False


class CharacterLanguages(models.Model):
    """
    This model maps to the character_languages table in the database
    """

    def __str__(self):
        return self.id

    id = models.IntegerField(primary_key=True, null=False, default=None)
    lang_id = models.SmallIntegerField(null=False, default=0)
    value = SmallIntegerField(null=False, default=0)

    class Meta:
        db_table = "character_languages"
        managed = False


class CharacterSkills(models.Model):
    """
    This model maps to the character_skills table in the database.
    """

    def __str__(self):
        return str(self.value)

    id = models.AutoField(primary_key=True)
    skill_id = models.PositiveSmallIntegerField(null=False, default=0)
    value = models.PositiveSmallIntegerField(null=False, default=0)

    class Meta:
        db_table = "character_skills"
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['id', 'skill_id'], name='unique_char_skill')
        ]


class CharacterSpells(models.Model):
    """
    This model maps to the character_spells table in the database.
    """

    def __str__(self):
        return str(self.spell_id_id)

    id = models.AutoField(primary_key=True)
    slot_id = models.PositiveSmallIntegerField(null=False, default=0)
    spell_id = models.ForeignKey(SpellsNew, on_delete=models.RESTRICT, db_column='spell_id')

    class Meta:
        db_table = 'character_spells'
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['id', 'slot_id'], name='unique_char_spell_slot')
        ]


