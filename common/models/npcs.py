from django.db import models
from common.models.items import Items


class NPCFaction(models.Model):
    """
    This model maps to the npc_faction table in the database
    """

    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True, null=False, default=None)
    name = models.TextField(null=True)
    primary_faction = models.IntegerField(null=False, default=0, db_column='primaryfaction')
    ignore_primary_assist = models.SmallIntegerField(null=False, default=0)

    class Meta:
        managed = False
        db_table = 'npc_faction'


class NPCFactionEntries(models.Model):
    """
    This model maps to the npc_faction_entries table in the database
    """
    def __str__(self):
        return str(self.npc_faction_id)

    npc_faction_id = models.PositiveIntegerField(null=False, primary_key=True, default=0)
    faction_id = models.PositiveIntegerField(null=False, default=0)
    value = models.IntegerField(null=False, default=0)
    npc_value = models.SmallIntegerField(null=False, default=0)
    temp = models.SmallIntegerField(null=False, default=0)

    class Meta:
        managed = False
        db_table = 'npc_faction_entries'
        constraints = [
            models.UniqueConstraint(fields=['npc_faction_id', 'faction_id'], name='unique_npc_faction_entry'),
        ]


class NPCSpellsEntries(models.Model):
    """
    This model maps to the npc_spells_entries table in the database
    """
    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True, null=False, default=None)
    npc_spells_id = models.IntegerField(null=False, default=0)
    spellid = models.PositiveSmallIntegerField(null=False, default=0)
    type = models.PositiveIntegerField(null=False, default=0)
    minlevel = models.PositiveSmallIntegerField(null=False, default=0)
    maxlevel = models.PositiveSmallIntegerField(null=False, default=255)
    manacost = models.SmallIntegerField(null=False, default=-1)
    recast_delay = models.IntegerField(null=False, default=-1)
    priority = models.SmallIntegerField(null=False, default=0)
    resist_adjust = models.IntegerField(null=True, default=None)
    min_hp = models.SmallIntegerField(null=True, default=0)
    max_hp = models.SmallIntegerField(null=True, default=0)
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        managed = False
        db_table = "npc_spells_entries"


class NPCTypes(models.Model):
    """
    This model maps to the npc_types table in the database.
    """

    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False)
    lastname = models.CharField(max_length=32, null=True, default=None)
    level = models.PositiveSmallIntegerField(null=False, default=0)
    race = models.PositiveSmallIntegerField(null=False, default=0)
    class_name = models.PositiveSmallIntegerField(null=False, default=0, db_column='class')
    bodytype = models.IntegerField(null=False, default=1)
    hp = models.BigIntegerField(null=False, default=0)
    mana = models.BigIntegerField(null=False, default=0)
    gender = models.PositiveSmallIntegerField(null=False, default=0)
    texture = models.PositiveSmallIntegerField(null=False, default=0)
    helmtexture = models.PositiveSmallIntegerField(null=False, default=0)
    herosforgemodel = models.IntegerField(null=False, default=0)
    size = models.FloatField(null=False, default=0)
    hp_regen_rate = models.BigIntegerField(null=False, default=0)
    hp_regen_per_second = models.BigIntegerField(null=False, default=0)
    mana_regen_rate = models.BigIntegerField(null=False, default=0)
    loottable_id = models.PositiveIntegerField(null=False, default=0)
    merchant_id = models.PositiveIntegerField(null=False, default=0)
    greed = models.PositiveSmallIntegerField(null=False, default=0)
    alt_currency_id = models.PositiveIntegerField(null=False, default=0)
    npc_spells_id = models.PositiveIntegerField(null=False, default=0)
    npc_spells_effects_id = models.PositiveIntegerField(null=False, default=0)
    npc_faction_id = models.IntegerField(null=False, default=0)
    adventure_template_id = models.PositiveIntegerField(null=False, default=0)
    trap_template = models.PositiveIntegerField(null=True, default=0)
    min_dmg = models.PositiveIntegerField(null=False, default=0, db_column='mindmg')
    max_dmg = models.PositiveIntegerField(null=False, default=0, db_column='maxdmg')
    attack_count = models.SmallIntegerField(null=False, default=-1)
    npcspecialattks = models.CharField(max_length=36, null=False, default='')
    special_abilities = models.TextField(null=True, default=None)
    aggroradius = models.PositiveIntegerField(null=False, default=0)
    assistradius = models.PositiveIntegerField(null=False, default=0)
    face = models.PositiveIntegerField(null=False, default=1)
    luclin_hairstyle = models.PositiveIntegerField(null=False, default=1)
    luclin_haircolor = models.PositiveIntegerField(null=False, default=1)
    luclin_eyecolor = models.PositiveIntegerField(null=False, default=1)
    luclin_eyecolor2 = models.PositiveIntegerField(null=False, default=1)
    luclin_beardcolor = models.PositiveIntegerField(null=False, default=1)
    luclin_beard = models.PositiveIntegerField(null=False, default=0)
    drakkin_heritage = models.IntegerField(null=False, default=0)
    drakkin_tattoo = models.IntegerField(null=False, default=0)
    drakkin_details = models.IntegerField(null=False, default=0)
    armortint_id = models.PositiveIntegerField(null=False, default=0)
    armortint_red = models.PositiveSmallIntegerField(null=False, default=0)
    armortint_green = models.PositiveSmallIntegerField(null=False, default=0)
    armortint_blue = models.PositiveSmallIntegerField(null=False, default=0)
    d_melee_texture1 = models.PositiveIntegerField(null=False, default=0)
    d_melee_texture2 = models.PositiveIntegerField(null=False, default=0)
    ammo_idfile = models.CharField(max_length=30, null=False, default='IT10')
    prim_melee_type = models.PositiveSmallIntegerField(null=False, default=28)
    sec_melee_type = models.PositiveSmallIntegerField(null=False, default=28)
    ranged_type = models.PositiveSmallIntegerField(null=False, default=7)
    runspeed = models.FloatField(null=False, default=0)
    MR = models.SmallIntegerField(null=False, default=0)
    CR = models.SmallIntegerField(null=False, default=0)
    DR = models.SmallIntegerField(null=False, default=0)
    FR = models.SmallIntegerField(null=False, default=0)
    PR = models.SmallIntegerField(null=False, default=0)
    Corrup = models.SmallIntegerField(null=False, default=0)
    PhR = models.PositiveSmallIntegerField(null=False, default=0)
    see_invis = models.SmallIntegerField(null=False, default=0)
    see_invis_undead = models.SmallIntegerField(null=False, default=0)
    qglobal = models.PositiveIntegerField(null=False, default=0)
    ac = models.SmallIntegerField(null=False, default=0, db_column='AC')
    npc_aggro = models.SmallIntegerField(null=False, default=0)
    spawn_limit = models.SmallIntegerField(null=False, default=0)
    attack_speed = models.FloatField(null=False, default=0)
    attack_delay = models.PositiveSmallIntegerField(null=False, default=30)
    findable = models.SmallIntegerField(null=False, default=0)
    STR = models.PositiveIntegerField(null=False, default=75)
    STA = models.PositiveIntegerField(null=False, default=75)
    DEX = models.PositiveIntegerField(null=False, default=75)
    AGI = models.PositiveIntegerField(null=False, default=75)
    intelligence = models.PositiveIntegerField(null=False, default=80, db_column='_INT')
    WIS = models.PositiveIntegerField(null=False, default=75)
    CHA = models.PositiveIntegerField(null=False, default=75)
    see_hide = models.SmallIntegerField(null=False, default=0)
    see_improved_hide = models.SmallIntegerField(null=False, default=0)
    trackable = models.SmallIntegerField(null=False, default=1)
    isbot = models.SmallIntegerField(null=False, default=0)
    exclude = models.SmallIntegerField(null=False, default=1)
    ATK = models.IntegerField(null=False, default=0)
    Accuracy = models.IntegerField(null=False, default=0)
    Avoidance = models.PositiveIntegerField(null=False, default=0)
    slow_mitigation = models.SmallIntegerField(null=False, default=0)
    version = models.PositiveSmallIntegerField(null=False, default=0)
    max_level = models.SmallIntegerField(null=False, default=0, db_column='maxlevel')
    scalerate = models.IntegerField(null=False, default=100)
    private_corpse = models.PositiveSmallIntegerField(null=False, default=0)
    unique_spawn_by_name = models.PositiveSmallIntegerField(null=False, default=0)
    underwater = models.PositiveSmallIntegerField(null=False, default=0)
    isquest = models.SmallIntegerField(null=False, default=0)
    emoteid = models.PositiveIntegerField(null=False, default=0)
    spellscale = models.FloatField(null=False, default=100)
    healscale = models.FloatField(null=False, default=100)
    no_target_hotkey = models.PositiveSmallIntegerField(null=False, default=0)
    raid_target = models.PositiveSmallIntegerField(null=False, default=0)
    armtexture = models.SmallIntegerField(null=False, default=0)
    bracertexture = models.SmallIntegerField(null=False, default=0)
    handtexture = models.SmallIntegerField(null=False, default=0)
    legtexture = models.SmallIntegerField(null=False, default=0)
    feettexture = models.SmallIntegerField(null=False, default=0)
    light = models.SmallIntegerField(null=False, default=0)
    walkspeed = models.FloatField(null=False, default=0)
    peqid = models.IntegerField(null=False, default=0)
    npc_unique = models.SmallIntegerField(null=False, default=0, db_column='unique_')
    fixed = models.SmallIntegerField(null=False, default=0)
    ignore_despawn = models.SmallIntegerField(null=False, default=0)
    show_name = models.SmallIntegerField(null=False, default=1)
    untargetable = models.SmallIntegerField(null=False, default=0)
    charm_ac = models.SmallIntegerField(null=True, default=0)
    charm_min_dmg = models.IntegerField(null=True, default=0)
    charm_max_dmg = models.IntegerField(null=True, default=0)
    charm_attack_delay = models.SmallIntegerField(null=True, default=0)
    charm_accuracy_rating = models.IntegerField(null=True, default=0)
    charm_avoidance_rating = models.IntegerField(null=True, default=0)
    charm_atk = models.IntegerField(null=True, default=0)
    skip_global_loot = models.SmallIntegerField(null=True, default=0)
    rare_spawn = models.SmallIntegerField(null=True, default=0)
    stuck_behavior = models.SmallIntegerField(null=False, default=0)
    npc_model = models.SmallIntegerField(null=False, default=0, db_column='model')
    flymode = models.SmallIntegerField(null=False, default=-1)
    always_aggro = models.PositiveSmallIntegerField(null=False, default=0)
    exp_mod = models.IntegerField(null=False, default=100)
    heroic_strikethrough = models.IntegerField(null=False, default=0)
    faction_amount = models.IntegerField(null=False, default=0)
    keeps_sold_items = models.PositiveSmallIntegerField(null=False, default=1)
    is_parcel_merchant = models.PositiveSmallIntegerField(null=False, default=0)
    multiquest_enabled = models.PositiveSmallIntegerField(null=False, default=0)
    npc_tint_id = models.PositiveSmallIntegerField(null=True, default=0)

    class Meta:
        db_table = "npc_types"
        managed = False


class MerchantList(models.Model):
    """
    This model maps to the merchantlist table in the database.
    """

    def __str__(self):
        return str(self.item)

    merchant_id = models.IntegerField(null=False, primary_key=True, default=0, db_column='merchantid')
    slot = models.PositiveIntegerField(null=False, default=0)
    item = models.ForeignKey(Items, on_delete=models.DO_NOTHING, db_column='item')
    faction_required = models.SmallIntegerField(null=False, default=-100)
    level_required = models.PositiveSmallIntegerField(null=False, default=0)
    min_status = models.PositiveSmallIntegerField(null=False, default=0)
    max_status = models.PositiveSmallIntegerField(null=False, default=255)
    alt_currency_cost = models.PositiveSmallIntegerField(null=False, default=0)
    classes_required = models.IntegerField(null=False, default=65535)
    probability = models.IntegerField(null=False, default=100)
    bucket_name = models.CharField(max_length=100, null=False, default='')
    bucket_value = models.CharField(max_length=100, null=False, default='')
    bucket_comparison = models.PositiveSmallIntegerField(null=True, default=0)
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = "merchantlist"
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['merchant_id', 'slot'], name='unique_merchant_slot'),
        ]


class MerchantListTemp(models.Model):
    """
    This model maps to the merchantlist_temp table in the database.
    """

    def __str__(self):
        return str(self.npc_id)

    npc_id = models.PositiveIntegerField(primary_key=True, null=False, default=0, db_column='npcid')
    slot = models.PositiveIntegerField(null=False, default=0)
    zone_id = models.IntegerField(null=False, default=0)
    instance_id = models.IntegerField(null=False, default=0)
    item_id = models.PositiveIntegerField(null=False, default=0, db_column='itemid')
    charges = models.PositiveIntegerField(null=False, default=1)

    class Meta:
        db_table = "merchantlist_temp"
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['npc_id', 'slot', 'zone_id', 'instance_id'], name='unique_temp_merchant'),
        ]
