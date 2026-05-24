from django.db import models


class Items(models.Model):
    """
    This model maps to the items table in the database.
    """

    def __str__(self):
        return str(self.id)

    # -----------------------------------------------------------------------
    # Core identity
    # -----------------------------------------------------------------------
    id = models.IntegerField(primary_key=True, null=False, default=0)
    minstatus = models.SmallIntegerField(null=False, default=0)
    Name = models.CharField(max_length=64, null=False, default='')
    idfile = models.CharField(max_length=30, null=False, default='')
    lore = models.CharField(max_length=80, null=False, default='')
    loregroup = models.IntegerField(null=False, default=0)
    lore_file = models.CharField(max_length=32, null=False, default='', db_column='lorefile')
    pendingloreflag = models.SmallIntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Classification
    # -----------------------------------------------------------------------
    item_class = models.IntegerField(null=False, default=0, db_column='itemclass')
    item_type = models.IntegerField(null=False, default=0, db_column='itemtype')
    subtype = models.IntegerField(null=False, default=0)
    slots = models.IntegerField(null=False, default=0)
    races = models.IntegerField(null=False, default=0)
    classes = models.IntegerField(null=False, default=0)
    deity = models.IntegerField(null=False, default=0)
    size = models.IntegerField(null=False, default=0)
    weight = models.IntegerField(null=False, default=0)
    material = models.IntegerField(null=False, default=0)
    herosforgemodel = models.IntegerField(null=False, default=0)
    color = models.PositiveIntegerField(null=False, default=0)
    light = models.IntegerField(null=False, default=0)
    icon = models.IntegerField(null=False, default=0)
    filename = models.CharField(max_length=32, null=False, default='')

    # -----------------------------------------------------------------------
    # Flags
    # -----------------------------------------------------------------------
    magic = models.IntegerField(null=False, default=0)
    no_drop = models.IntegerField(null=False, default=0, db_column='nodrop')
    no_rent = models.IntegerField(null=False, default=0, db_column='norent')
    notransfer = models.IntegerField(null=False, default=0)
    attuneable = models.IntegerField(null=False, default=0)
    nopet = models.IntegerField(null=False, default=0)
    fv_nodrop = models.IntegerField(null=False, default=0, db_column='fvnodrop')
    artifactflag = models.SmallIntegerField(null=False, default=0)
    summonedflag = models.SmallIntegerField(null=False, default=0)
    quest_item_flag = models.IntegerField(null=False, default=0, db_column='questitemflag')
    heirloom = models.IntegerField(null=False, default=0)
    placeable = models.IntegerField(null=False, default=0)
    epicitem = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Stats
    # -----------------------------------------------------------------------
    ac = models.IntegerField(null=False, default=0)
    hp = models.IntegerField(null=False, default=0)
    mana = models.IntegerField(null=False, default=0)
    endur = models.IntegerField(null=False, default=0)
    regen = models.IntegerField(null=False, default=0)
    manaregen = models.IntegerField(null=False, default=0)
    enduranceregen = models.IntegerField(null=False, default=0)
    astr = models.IntegerField(null=False, default=0)
    adex = models.IntegerField(null=False, default=0)
    asta = models.IntegerField(null=False, default=0)
    aagi = models.IntegerField(null=False, default=0)
    aint = models.IntegerField(null=False, default=0)
    awis = models.IntegerField(null=False, default=0)
    acha = models.IntegerField(null=False, default=0)
    fr = models.IntegerField(null=False, default=0)
    dr = models.IntegerField(null=False, default=0)
    cr = models.IntegerField(null=False, default=0)
    mr = models.IntegerField(null=False, default=0)
    pr = models.IntegerField(null=False, default=0)
    svcorruption = models.IntegerField(null=False, default=0)
    haste = models.IntegerField(null=False, default=0)
    attack = models.IntegerField(null=False, default=0)
    accuracy = models.IntegerField(null=False, default=0)
    avoidance = models.IntegerField(null=False, default=0)
    shielding = models.IntegerField(null=False, default=0)
    spellshield = models.IntegerField(null=False, default=0)
    strikethrough = models.IntegerField(null=False, default=0)
    stunresist = models.IntegerField(null=False, default=0)
    dotshielding = models.IntegerField(null=False, default=0)
    damageshield = models.IntegerField(null=False, default=0)
    dsmitigation = models.SmallIntegerField(null=False, default=0)
    purity = models.IntegerField(null=False, default=0)

    # Heroic stats
    heroic_str = models.SmallIntegerField(null=False, default=0)
    heroic_int = models.SmallIntegerField(null=False, default=0)
    heroic_wis = models.SmallIntegerField(null=False, default=0)
    heroic_agi = models.SmallIntegerField(null=False, default=0)
    heroic_dex = models.SmallIntegerField(null=False, default=0)
    heroic_sta = models.SmallIntegerField(null=False, default=0)
    heroic_cha = models.SmallIntegerField(null=False, default=0)
    heroic_pr = models.SmallIntegerField(null=False, default=0)
    heroic_dr = models.SmallIntegerField(null=False, default=0)
    heroic_fr = models.SmallIntegerField(null=False, default=0)
    heroic_cr = models.SmallIntegerField(null=False, default=0)
    heroic_mr = models.SmallIntegerField(null=False, default=0)
    heroic_svcorrup = models.SmallIntegerField(null=False, default=0)
    healamt = models.SmallIntegerField(null=False, default=0)
    spelldmg = models.SmallIntegerField(null=False, default=0)
    clairvoyance = models.SmallIntegerField(null=False, default=0)
    backstabdmg = models.SmallIntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Combat
    # -----------------------------------------------------------------------
    damage = models.IntegerField(null=False, default=0)
    delay = models.IntegerField(null=False, default=0)
    range = models.IntegerField(null=False, default=0)
    bane_dmg_amt = models.IntegerField(null=False, default=0, db_column='banedmgamt')
    banedmgraceamt = models.IntegerField(null=False, default=0)
    bane_dmg_body = models.IntegerField(null=False, default=0, db_column='banedmgbody')
    bane_dmg_race = models.IntegerField(null=False, default=0, db_column='banedmgrace')
    extradmgskill = models.IntegerField(null=False, default=0)
    extradmgamt = models.IntegerField(null=False, default=0)
    elem_dmg_type = models.IntegerField(null=False, default=0, db_column='elemdmgtype')
    elem_dmg_amt = models.IntegerField(null=False, default=0, db_column='elemdmgamt')
    combateffects = models.CharField(max_length=10, null=False, default='')
    proc_rate = models.IntegerField(null=False, default=0, db_column='procrate')

    # -----------------------------------------------------------------------
    # Economy
    # -----------------------------------------------------------------------
    price = models.IntegerField(null=False, default=0)
    sell_rate = models.FloatField(null=False, default=0, db_column='sellrate')
    tradeskills = models.IntegerField(null=False, default=0)
    ldonprice = models.IntegerField(null=False, default=0)
    ldontheme = models.IntegerField(null=False, default=0)
    ldonsold = models.IntegerField(null=False, default=0)
    ldonsellbackrate = models.SmallIntegerField(null=False, default=0)
    guildfavor = models.IntegerField(null=False, default=0)
    favor = models.IntegerField(null=False, default=0)
    pointtype = models.IntegerField(null=False, default=0)
    potionbelt = models.IntegerField(null=False, default=0)
    potionbeltslots = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Requirements
    # -----------------------------------------------------------------------
    req_level = models.IntegerField(null=False, default=0, db_column='reqlevel')
    rec_level = models.IntegerField(null=False, default=0, db_column='reclevel')
    rec_skill = models.IntegerField(null=False, default=0, db_column='recskill')
    skill_mod_type = models.IntegerField(null=False, default=0, db_column='skillmodtype')
    skill_mod_value = models.IntegerField(null=False, default=0, db_column='skillmodvalue')
    skillmodmax = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Container
    # -----------------------------------------------------------------------
    bag_size = models.IntegerField(null=False, default=0, db_column='bagsize')
    bag_slots = models.IntegerField(null=False, default=0, db_column='bagslots')
    bag_type = models.IntegerField(null=False, default=0, db_column='bagtype')
    bag_wr = models.IntegerField(null=False, default=0, db_column='bagwr')

    # -----------------------------------------------------------------------
    # Charges / stacking
    # -----------------------------------------------------------------------
    max_charges = models.IntegerField(null=False, default=0, db_column='maxcharges')
    stackable = models.IntegerField(null=False, default=0)
    stacksize = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Book
    # -----------------------------------------------------------------------
    book = models.IntegerField(null=False, default=0)
    booktype = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Evolving items
    # -----------------------------------------------------------------------
    evoitem = models.IntegerField(null=False, default=0)
    evoid = models.IntegerField(null=False, default=0)
    evolvinglevel = models.IntegerField(null=False, default=0)
    evomax = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Power source / misc display
    # -----------------------------------------------------------------------
    powersourcecapacity = models.IntegerField(null=False, default=0)
    expendablearrow = models.SmallIntegerField(null=False, default=0)
    elitematerial = models.SmallIntegerField(null=False, default=0)
    scriptfileid = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Faction
    # -----------------------------------------------------------------------
    faction_mod1 = models.IntegerField(null=False, default=0, db_column='factionmod1')
    faction_mod2 = models.IntegerField(null=False, default=0, db_column='factionmod2')
    faction_mod3 = models.IntegerField(null=False, default=0, db_column='factionmod3')
    faction_mod4 = models.IntegerField(null=False, default=0, db_column='factionmod4')
    faction_amt1 = models.IntegerField(null=False, default=0, db_column='factionamt1')
    faction_amt2 = models.IntegerField(null=False, default=0, db_column='factionamt2')
    faction_amt3 = models.IntegerField(null=False, default=0, db_column='factionamt3')
    faction_amt4 = models.IntegerField(null=False, default=0, db_column='factionamt4')

    # -----------------------------------------------------------------------
    # Click effect
    # -----------------------------------------------------------------------
    click_effect = models.IntegerField(null=False, default=0, db_column='clickeffect')
    click_type = models.IntegerField(null=False, default=0, db_column='clicktype')
    click_level = models.IntegerField(null=False, default=0, db_column='clicklevel')
    click_level2 = models.IntegerField(null=False, default=0, db_column='clicklevel2')
    clickname = models.CharField(max_length=64, null=False, default='')
    clickunk5 = models.IntegerField(null=False, default=0)
    clickunk6 = models.CharField(max_length=32, null=False, default='')
    clickunk7 = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Proc effect
    # -----------------------------------------------------------------------
    proc_effect = models.IntegerField(null=False, default=0, db_column='proceffect')
    proc_type = models.IntegerField(null=False, default=0, db_column='proctype')
    proc_level = models.IntegerField(null=False, default=0, db_column='proclevel')
    proc_level2 = models.IntegerField(null=False, default=0, db_column='proclevel2')
    procname = models.CharField(max_length=64, null=False, default='')
    procunk1 = models.IntegerField(null=False, default=0)
    procunk2 = models.IntegerField(null=False, default=0)
    procunk3 = models.IntegerField(null=False, default=0)
    procunk4 = models.IntegerField(null=False, default=0)
    procunk6 = models.CharField(max_length=32, null=False, default='')
    procunk7 = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Worn effect
    # -----------------------------------------------------------------------
    worn_effect = models.IntegerField(null=False, default=0, db_column='worneffect')
    worn_type = models.IntegerField(null=False, default=0, db_column='worntype')
    worn_level = models.IntegerField(null=False, default=0, db_column='wornlevel')
    worn_level2 = models.IntegerField(null=False, default=0, db_column='wornlevel2')
    wornname = models.CharField(max_length=64, null=False, default='')
    wornunk1 = models.IntegerField(null=False, default=0)
    wornunk2 = models.IntegerField(null=False, default=0)
    wornunk3 = models.IntegerField(null=False, default=0)
    wornunk4 = models.IntegerField(null=False, default=0)
    wornunk5 = models.IntegerField(null=False, default=0)
    wornunk6 = models.CharField(max_length=32, null=False, default='')
    wornunk7 = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Focus effect
    # -----------------------------------------------------------------------
    focus_effect = models.IntegerField(null=False, default=0, db_column='focuseffect')
    focus_type = models.IntegerField(null=False, default=0, db_column='focustype')
    focus_level = models.IntegerField(null=False, default=0, db_column='focuslevel')
    focus_level2 = models.IntegerField(null=False, default=0, db_column='focuslevel2')
    focusname = models.CharField(max_length=64, null=False, default='')
    focusunk1 = models.IntegerField(null=False, default=0)
    focusunk2 = models.IntegerField(null=False, default=0)
    focusunk3 = models.IntegerField(null=False, default=0)
    focusunk4 = models.IntegerField(null=False, default=0)
    focusunk5 = models.IntegerField(null=False, default=0)
    focusunk6 = models.CharField(max_length=32, null=False, default='')
    focusunk7 = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Scroll effect
    # -----------------------------------------------------------------------
    scroll_effect = models.IntegerField(null=False, default=0, db_column='scrolleffect')
    scroll_type = models.IntegerField(null=False, default=0, db_column='scrolltype')
    scroll_level = models.IntegerField(null=False, default=0, db_column='scrolllevel')
    scroll_level2 = models.IntegerField(null=False, default=0, db_column='scrolllevel2')
    scrollname = models.CharField(max_length=64, null=False, default='')
    scrollunk1 = models.PositiveIntegerField(null=False, default=0)
    scrollunk2 = models.IntegerField(null=False, default=0)
    scrollunk3 = models.IntegerField(null=False, default=0)
    scrollunk4 = models.IntegerField(null=False, default=0)
    scrollunk5 = models.IntegerField(null=False, default=0)
    scrollunk6 = models.CharField(max_length=32, null=False, default='')
    scrollunk7 = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Cast time (shared)
    # -----------------------------------------------------------------------
    cast_time = models.IntegerField(null=False, default=0, db_column='casttime')
    cast_time2 = models.IntegerField(null=False, default=0, db_column='casttime_')
    recast_delay = models.IntegerField(null=False, default=0, db_column='recastdelay')
    recast_type = models.IntegerField(null=False, default=0, db_column='recasttype')

    # -----------------------------------------------------------------------
    # Bard effect
    # -----------------------------------------------------------------------
    bard_type = models.IntegerField(null=False, default=0, db_column='bardtype')
    bard_value = models.IntegerField(null=False, default=0, db_column='bardvalue')
    bard_effect = models.IntegerField(null=False, default=0, db_column='bardeffect')
    bard_effect_type = models.SmallIntegerField(null=False, default=0, db_column='bardeffecttype')
    bard_level = models.SmallIntegerField(null=False, default=0, db_column='bardlevel')
    bard_level2 = models.SmallIntegerField(null=False, default=0, db_column='bardlevel2')
    bardname = models.CharField(max_length=64, null=False, default='')
    bardunk1 = models.SmallIntegerField(null=False, default=0)
    bardunk2 = models.SmallIntegerField(null=False, default=0)
    bardunk3 = models.SmallIntegerField(null=False, default=0)
    bardunk4 = models.SmallIntegerField(null=False, default=0)
    bardunk5 = models.SmallIntegerField(null=False, default=0)
    bardunk7 = models.SmallIntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Augmentation
    # -----------------------------------------------------------------------
    augrestrict = models.IntegerField(null=False, default=0)
    augtype = models.IntegerField(null=False, default=0)
    augdistiller = models.PositiveIntegerField(null=False, default=0)
    augslot1type = models.SmallIntegerField(null=False, default=0)
    augslot1visible = models.SmallIntegerField(null=False, default=0)
    augslot1unk2 = models.IntegerField(null=False, default=0)
    augslot2type = models.SmallIntegerField(null=False, default=0)
    augslot2visible = models.SmallIntegerField(null=False, default=0)
    augslot2unk2 = models.IntegerField(null=False, default=0)
    augslot3type = models.SmallIntegerField(null=False, default=0)
    augslot3visible = models.SmallIntegerField(null=False, default=0)
    augslot3unk2 = models.IntegerField(null=False, default=0)
    augslot4type = models.SmallIntegerField(null=False, default=0)
    augslot4visible = models.SmallIntegerField(null=False, default=0)
    augslot4unk2 = models.IntegerField(null=False, default=0)
    augslot5type = models.SmallIntegerField(null=False, default=0)
    augslot5visible = models.SmallIntegerField(null=False, default=0)
    augslot5unk2 = models.IntegerField(null=False, default=0)
    augslot6type = models.SmallIntegerField(null=False, default=0)
    augslot6visible = models.SmallIntegerField(null=False, default=0)
    augslot6unk2 = models.IntegerField(null=False, default=0)

    # -----------------------------------------------------------------------
    # Metadata
    # -----------------------------------------------------------------------
    source = models.CharField(max_length=20, null=False, default='')
    charmfile = models.CharField(max_length=32, null=False, default='')
    charmfileid = models.CharField(max_length=32, null=False, default='')
    comment = models.CharField(max_length=255, null=False, default='')
    created = models.CharField(max_length=64, null=False, default='')
    updated = models.DateTimeField(null=True, blank=True)
    serialized = models.DateTimeField(null=True, blank=True)
    verified = models.DateTimeField(null=True, blank=True)
    serialization = models.TextField(null=True, blank=True)

    # -----------------------------------------------------------------------
    # Unknown / reserved fields
    # -----------------------------------------------------------------------
    benefitflag = models.IntegerField(null=False, default=0)
    unk012 = models.IntegerField(null=False, default=0, db_column='UNK012')
    unk013 = models.IntegerField(null=False, default=0, db_column='UNK013')
    unk014 = models.IntegerField(null=False, default=0, db_column='UNK014')
    unk033 = models.IntegerField(null=False, default=0, db_column='UNK033')
    unk054 = models.IntegerField(null=False, default=0, db_column='UNK054')
    unk059 = models.IntegerField(null=False, default=0, db_column='UNK059')
    unk060 = models.IntegerField(null=False, default=0, db_column='UNK060')
    unk120 = models.IntegerField(null=False, default=0, db_column='UNK120')
    unk121 = models.IntegerField(null=False, default=0, db_column='UNK121')
    unk123 = models.IntegerField(null=False, default=0, db_column='UNK123')
    unk124 = models.IntegerField(null=False, default=0, db_column='UNK124')
    unk127 = models.IntegerField(null=False, default=0, db_column='UNK127')
    unk132 = models.TextField(null=True, blank=True, db_column='UNK132')
    unk134 = models.CharField(max_length=255, null=False, default='', db_column='UNK134')
    unk137 = models.IntegerField(null=False, default=0, db_column='UNK137')
    unk142 = models.IntegerField(null=False, default=0, db_column='UNK142')
    unk147 = models.IntegerField(null=False, default=0, db_column='UNK147')
    unk152 = models.IntegerField(null=False, default=0, db_column='UNK152')
    unk157 = models.IntegerField(null=False, default=0, db_column='UNK157')
    unk193 = models.IntegerField(null=False, default=0, db_column='UNK193')
    unk214 = models.SmallIntegerField(null=False, default=0, db_column='UNK214')
    unk220 = models.IntegerField(null=False, default=0, db_column='UNK220')
    unk221 = models.IntegerField(null=False, default=0, db_column='UNK221')
    unk223 = models.IntegerField(null=False, default=0, db_column='UNK223')
    unk224 = models.IntegerField(null=False, default=0, db_column='UNK224')
    unk225 = models.IntegerField(null=False, default=0, db_column='UNK225')
    unk226 = models.IntegerField(null=False, default=0, db_column='UNK226')
    unk227 = models.IntegerField(null=False, default=0, db_column='UNK227')
    unk228 = models.IntegerField(null=False, default=0, db_column='UNK228')
    unk229 = models.IntegerField(null=False, default=0, db_column='UNK229')
    unk230 = models.IntegerField(null=False, default=0, db_column='UNK230')
    unk231 = models.IntegerField(null=False, default=0, db_column='UNK231')
    unk232 = models.IntegerField(null=False, default=0, db_column='UNK232')
    unk233 = models.IntegerField(null=False, default=0, db_column='UNK233')
    unk234 = models.IntegerField(null=False, default=0, db_column='UNK234')
    unk236 = models.IntegerField(null=False, default=0, db_column='UNK236')
    unk237 = models.IntegerField(null=False, default=0, db_column='UNK237')
    unk238 = models.IntegerField(null=False, default=0, db_column='UNK238')
    unk239 = models.IntegerField(null=False, default=0, db_column='UNK239')
    unk240 = models.IntegerField(null=False, default=0, db_column='UNK240')
    unk241 = models.IntegerField(null=False, default=0, db_column='UNK241')

    class Meta:
        db_table = 'items'
        managed = False

    # -----------------------------------------------------------------------
    # Display helpers
    # -----------------------------------------------------------------------

    def get_slot_display(self):
        """Convert slots bitfield to readable format"""
        if not self.slots:
            return ""

        slot_checks = [
            ([2, 16], "EARS"),
            ([4], "HEAD"),
            ([8], "FACE"),
            ([32], "NECK"),
            ([64], "SHOULDER"),
            ([128], "ARMS"),
            ([256], "BACK"),
            ([512, 1024], "WRIST"),
            ([2048], "RANGE"),
            ([4096], "HANDS"),
            ([8192], "PRIMARY"),
            ([16384], "SECONDARY"),
            ([32768, 65536], "FINGERS"),
            ([131072], "CHEST"),
            ([262144], "LEGS"),
            ([524288], "FEET"),
            ([1048576], "WAIST"),
            ([2097152], "POWERSOURCE"),
            ([4194304], "AMMO"),
        ]

        slots_available = [
            slot_name for bits, slot_name in slot_checks
            if any(self.slots & bit for bit in bits)
        ]

        return " ".join(slots_available)

    def get_item_type_display(self):
        """Convert item type to readable format"""
        type_mapping = {
            0: "1H Slashing", 1: "2H Slashing", 2: "1H Piercing",
            3: "1H Blunt", 4: "2H Blunt", 5: "Archery", 6: "Shield",
            7: "Armor", 8: "Misc", 9: "Lockpicks", 10: "Unused",
            11: "1H Piercing", 12: "Unused", 13: "Unused", 14: "Unused",
            15: "Unused", 16: "Unused", 17: "Unused", 18: "Unused",
            19: "Unused", 20: "Thrown", 21: "Bow", 22: "Unused",
            23: "Key", 24: "Unused", 25: "Unused", 26: "Unused",
            27: "Unused", 28: "Unused", 29: "Unused", 30: "Unused",
            31: "Unused", 32: "Unused", 33: "Unused", 34: "Unused",
            35: "2H Piercing"
        }
        return type_mapping.get(self.item_type, f"Unknown ({self.item_type})")

    def get_class_restrictions_display(self):
        """Convert classes bitfield to readable format"""
        if not self.classes or self.classes == 32767:  # 32767 = all classes
            return ""

        class_mapping = {
            1: "WAR", 2: "CLR", 4: "PAL", 8: "RNG", 16: "SHD",
            32: "DRU", 64: "MNK", 128: "BRD", 256: "ROG", 512: "SHM",
            1024: "NEC", 2048: "WIZ", 4096: "MAG", 8192: "ENC", 16384: "BST"
        }

        classes = []
        for bit_value, class_name in class_mapping.items():
            if self.classes & bit_value:
                classes.append(class_name)

        return " ".join(classes)

    def get_race_restrictions_display(self):
        """Convert races bitfield to readable format"""
        if not self.races or self.races == 16383:  # All races
            return ""

        race_mapping = {
            1: "HUM", 2: "BAR", 4: "ERU", 8: "ELF", 16: "HIE", 32: "DEF",
            64: "HEF", 128: "DWF", 256: "TRL", 512: "OGR", 1024: "HFL",
            2048: "GNM", 4096: "IKS", 8192: "VAH"
        }

        races = []
        for bit_value, race_name in race_mapping.items():
            if self.races & bit_value:
                races.append(race_name)

        return " ".join(races)

    def get_size_display(self):
        """Convert size to readable format"""
        size_mapping = {0: "TINY", 1: "SMALL", 2: "MEDIUM", 3: "LARGE", 4: "GIANT"}
        return size_mapping.get(self.size, "UNKNOWN")

    def get_weight_display(self):
        """Convert weight to readable format with decimal handling"""
        if self.weight == 0:
            return "0.0"
        elif self.weight < 10:
            return f"0.{self.weight}"
        else:
            return f"{self.weight // 10}.{self.weight % 10}"

    def format_stat_value(self, value):
        """Format stat values with proper +/- prefix"""
        if value > 0:
            return f"+{value}"
        return str(value)

    def generate_og_description(self, effect_name=None, focus_effect_name=None):
        """Generate Open Graph description for Discord/social media"""
        lines = []

        # Item flags row
        flags = []
        if self.magic:
            flags.append("MAGIC ITEM")
        if self.no_rent == 0:
            flags.append("NO RENT")
        if self.lore and self.lore.startswith('*'):
            flags.append("LORE ITEM")
        if self.no_drop == 0:
            flags.append("NODROP")

        if flags:
            lines.append(" ".join(flags))

        # Slot information
        slot_display = self.get_slot_display()
        if slot_display:
            lines.append(f"Slot: {slot_display}")

        # Skill and delay - only for weapons
        skill_delay_parts = []
        weapon_types = [0, 1, 2, 3, 4, 5, 35]
        if self.item_type in weapon_types:
            type_display = self.get_item_type_display()
            if "Unknown" not in type_display:
                skill_delay_parts.append(f"Skill: {type_display}")
        if self.delay:
            skill_delay_parts.append(f"Atk Delay: {self.delay}")

        if skill_delay_parts:
            lines.append(" ".join(skill_delay_parts))

        if self.damage:
            lines.append(f"DMG: {self.damage}")

        if self.max_charges > 0:
            lines.append(f"Charges: {self.max_charges}")

        if self.ac:
            lines.append(f"AC: {self.ac}")

        stats = []
        stat_fields = [
            (self.astr, 'STR'), (self.adex, 'DEX'), (self.asta, 'STA'),
            (self.acha, 'CHA'), (self.awis, 'WIS'), (self.aint, 'INT'),
            (self.aagi, 'AGI'), (self.hp, 'HP')
        ]
        for value, display in stat_fields:
            if value:
                stats.append(f"{display}: {self.format_stat_value(value)}")
        if self.mana:
            stats.append(f"MANA: +{self.mana}")
        if stats:
            lines.append(" ".join(stats))

        resists = []
        resist_fields = [
            (self.fr, 'SV FIRE'), (self.dr, 'SV DISEASE'), (self.cr, 'SV COLD'),
            (self.mr, 'SV MAGIC'), (self.pr, 'SV POISON')
        ]
        for value, display in resist_fields:
            if value:
                resists.append(f"{display}: +{value}")
        if resists:
            lines.append(" ".join(resists))

        focus_mods = []
        if self.skill_mod_value and self.skill_mod_value != 0:
            skill_name = self.get_skill_mod_display()
            focus_mods.append(f"Skill Mod: {skill_name} +{self.skill_mod_value}%")
        if self.focus_effect and self.focus_effect > 0:
            if focus_effect_name:
                focus_mods.append(f"Focus: {focus_effect_name}")
            else:
                focus_mods.append(f"Focus Effect: {self.focus_effect}")
        if focus_mods:
            lines.extend(focus_mods)

        if effect_name:
            effects = []
            if self.click_type in [1, 3, 4, 5]:
                cast_time = "Instant" if self.cast_time in [0, -1] else f"{self.cast_time / 1000:.1f} sec"
                if self.click_type == 1:
                    detail = f"(Any Slot, Casting Time: {cast_time})"
                elif self.click_type == 4:
                    detail = f"(Must Equip, Casting Time: {cast_time})"
                else:
                    detail = f"(Casting Time: {cast_time})"
                effects.append(f"Effect: {effect_name} {detail}")
            if self.worn_type == 2:
                worn_effect = f"Effect: {effect_name} (Worn)"
                if self.worn_effect == 998 and self.worn_level:
                    worn_effect += f" ({self.worn_level + 1}%)"
                effects.append(worn_effect)
            if self.proc_type == 0 and self.proc_effect > 0:
                cast_time = "Instant" if self.cast_time == 0 else f"{self.cast_time / 1000:.1f} sec"
                effects.append(f"Effect: {effect_name} (Combat, Casting Time: {cast_time}) at Level {self.proc_level}")
            if effects:
                lines.extend(effects)

        if self.rec_level:
            lines.append(f"Recommended level of {self.rec_level}.")

        weight_parts = [f"WT: {self.get_weight_display()}"]
        if self.bag_type:
            if self.bag_wr:
                weight_parts.append(f"Weight Reduction: {self.bag_wr}%")
            weight_parts.append(f"Capacity: {self.bag_slots}")
            weight_parts.append(f"Size Capacity: {self.get_size_display()}")
        else:
            weight_parts.append(f"Size: {self.get_size_display()}")
        lines.append(" ".join(weight_parts))

        class_display = self.get_class_restrictions_display()
        if class_display:
            lines.append(f"Class: {class_display}")

        race_display = self.get_race_restrictions_display()
        if race_display:
            lines.append(f"Race: {race_display}")

        return "\n".join(lines)

    def get_skill_mod_display(self):
        """Convert skill_mod_type to readable format"""
        skill_mapping = {
            0: "1H Blunt", 1: "1H Slashing", 2: "2H Blunt", 3: "2H Slashing",
            4: "Abjuration", 5: "Alteration", 6: "Apply Poison", 7: "Archery",
            8: "Backstab", 9: "Bind Wound", 10: "Bash", 11: "Block",
            12: "Brass Instruments", 13: "Channeling", 14: "Conjuration",
            15: "Defense", 16: "Disarm", 17: "Disarm Traps", 18: "Divination",
            19: "Dodge", 20: "Double Attack", 21: "Dragon Punch", 22: "Dual Wield",
            23: "Eagle Strike", 24: "Evocation", 25: "Feign Death", 26: "Flying Kick",
            27: "Forage", 28: "Hand to Hand", 29: "Hide", 30: "Kick",
            31: "Meditate", 32: "Mend", 33: "Offense", 34: "Parry",
            35: "Pick Lock", 36: "1H Piercing", 37: "Riposte", 38: "Round Kick",
            39: "Safe Fall", 40: "Sense Heading", 41: "Singing", 42: "Sneak",
            43: "Specialize Abjure", 44: "Specialize Alteration", 45: "Specialize Conjuration",
            46: "Specialize Divination", 47: "Specialize Evocation", 48: "Pick Pockets",
            49: "Stringed Instruments", 50: "Swimming", 51: "Throwing", 52: "Tiger Claw",
            53: "Tracking", 54: "Wind Instruments", 55: "Fishing", 56: "Make Poison",
            57: "Tinkering", 58: "Research", 59: "Alchemy", 60: "Baking",
            61: "Tailoring", 62: "Sense Traps", 63: "Blacksmithing", 64: "Fletching",
            65: "Brewing", 66: "Alcohol Tolerance", 67: "Begging", 68: "Jewelrymaking",
            69: "Pottery", 70: "Percussion Instruments", 71: "Intimidation",
            72: "Berserking", 73: "Taunt"
        }
        return skill_mapping.get(self.skill_mod_type, f"Unknown Skill ({self.skill_mod_type})")

    def get_clean_name(self):
        """Remove underscores and prepended # from item names"""
        if self.Name:
            cleaned = self.Name.replace('_', ' ')
            return cleaned.replace('#', '')
        return self.Name


class DiscoveredItems(models.Model):
    """
    This model maps to the discovered_items table in the database.
    """
    item_id = models.OneToOneField(Items, on_delete=models.DO_NOTHING, primary_key=True, db_column='item_id')
    char_name = models.CharField(max_length=64, null=False)
    discovered_date = models.PositiveIntegerField(null=False, default=0)
    account_status = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'discovered_items'
        managed = False
