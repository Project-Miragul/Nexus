from django.db import models

from common.models.npcs import NPCTypes


class SpawnGroup(models.Model):
    """
    This model maps to the spawngroup table in the database.
    """

    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, unique=True)
    spawn_limit = models.SmallIntegerField(null=False, default=0)
    dist = models.FloatField(null=False, default=0)
    max_x = models.FloatField(null=False, default=0)
    min_x = models.FloatField(null=False, default=0)
    max_y = models.FloatField(null=False, default=0)
    min_y = models.FloatField(null=False, default=0)
    delay = models.IntegerField(null=False, default=45000)
    min_delay = models.IntegerField(null=False, default=15000, db_column="mindelay")
    despawn = models.SmallIntegerField(null=False, default=0)
    despawn_timer = models.IntegerField(null=False, default=100)
    wp_spawns = models.PositiveSmallIntegerField(null=False, default=0)

    class Meta:
        db_table = "spawngroup"
        managed = False


class SpawnEntry(models.Model):
    """
    This model maps to the spawnentry table in the database.
    """

    def __str__(self):
        return str(self.spawngroupID)

    spawngroupID = models.IntegerField(primary_key=True, null=False, default=0)
    npcID = models.ForeignKey(NPCTypes, null=False, default=0, on_delete=models.RESTRICT, db_column='npcID')
    chance = models.SmallIntegerField(null=False, default=0)
    condition_value_filter = models.IntegerField(null=False, default=1)
    min_time = models.SmallIntegerField(null=False, default=0)
    max_time = models.SmallIntegerField(null=False, default=0)
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = "spawnentry"
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['spawngroupID', 'npcID'], name='unique_spawngroup_npc')
        ]


class Spawn2(models.Model):
    """
    This model maps to the spawn2 table in the database.
    """

    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True)
    spawngroupID = models.IntegerField(null=False, default=0)
    zone = models.CharField(max_length=32, null=True, default=None)
    version = models.SmallIntegerField(null=False, default=0)
    x = models.FloatField(null=False, default=0.0)
    y = models.FloatField(null=False, default=0.0)
    z = models.FloatField(null=False, default=0.0)
    heading = models.FloatField(null=False, default=0.0)
    respawntime = models.IntegerField(null=False, default=0)
    variance = models.IntegerField(null=False, default=0)
    pathgrid = models.IntegerField(null=False, default=0)
    path_when_zone_idle = models.PositiveSmallIntegerField(null=False, default=0)
    _condition = models.PositiveIntegerField(null=False, default=0)
    cond_value = models.IntegerField(null=False, default=1)
    animation = models.PositiveSmallIntegerField(null=False, default=0)
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = "spawn2"
        managed = False
