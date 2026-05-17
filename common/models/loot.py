from django.db import models

from common.models.items import Items


class LootTable(models.Model):
    """
    This model maps to the loottable table in the database.
    """
    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, default='')
    min_cash = models.PositiveIntegerField(null=False, default=0, db_column='mincash')
    max_cash = models.PositiveIntegerField(null=False, default=0, db_column='maxcash')
    avg_coin = models.PositiveIntegerField(null=False, default=0, db_column='avgcoin')
    done = models.SmallIntegerField(null=False, default=0)
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = 'loottable'
        managed = False


class LootDrop(models.Model):
    """
    This model maps to the lootdrop table in the database.
    """
    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, default='')
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = 'lootdrop'
        managed = False


class LootTableEntries(models.Model):
    """
    This model maps to the loottable_entries table in the database.
    """
    def __str__(self):
        return str(self.lootdrop_id.id)

    loottable_id = models.PositiveIntegerField(primary_key=True, null=False, default=0)
    lootdrop_id = models.ForeignKey(LootDrop, models.DO_NOTHING, db_column='lootdrop_id')
    multiplier = models.PositiveSmallIntegerField(null=False, default=1)
    probability = models.FloatField(null=False, default=100)
    drop_limit = models.PositiveSmallIntegerField(null=False, default=0, db_column='droplimit')
    min_drop = models.PositiveSmallIntegerField(null=False, default=0, db_column='mindrop')

    class Meta:
        db_table = 'loottable_entries'
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['loottable_id', 'lootdrop_id'], name='unique_loottable_entry'),
        ]


class LootDropEntries(models.Model):
    """
    This model maps to the lootdrop_entries table in the database
    """
    def __str__(self):
        return str(self.item_id.Name)

    lootdrop_id = models.PositiveIntegerField(primary_key=True, null=False, default=0)
    item_id = models.ForeignKey(Items, models.DO_NOTHING, db_column='item_id')
    item_charges = models.PositiveSmallIntegerField(null=False, default=1)
    equip_item = models.PositiveSmallIntegerField(null=False, default=0)
    chance = models.FloatField(null=False, default=1)
    disabled_chance = models.FloatField(null=False, default=0)
    trivial_min_level = models.PositiveSmallIntegerField(null=False, default=0)
    trivial_max_level = models.PositiveSmallIntegerField(null=False, default=0)
    multiplier = models.PositiveSmallIntegerField(null=False, default=1)
    npc_min_level = models.PositiveSmallIntegerField(null=False, default=0)
    npc_max_level = models.PositiveSmallIntegerField(null=False, default=0)
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = 'lootdrop_entries'
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['lootdrop_id', 'item_id'], name='unique_lootdrop_entry'),
        ]
