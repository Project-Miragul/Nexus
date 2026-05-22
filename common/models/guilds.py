from django.db import models
from common.models.characters import Characters


class Guilds(models.Model):
    """
    This model maps to the guilds table in the database
    """

    def __str__(self):
        return str(self.name)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False, unique=True)
    leader = models.IntegerField(null=False, unique=True, default=0)
    minstatus = models.SmallIntegerField(null=False, default=0)
    motd = models.TextField(null=False)
    tribute = models.PositiveIntegerField(null=False, default=0)
    motd_setter = models.CharField(max_length=64, null=False, default='')
    channel = models.CharField(max_length=128, null=False, default='')
    url = models.CharField(max_length=512, null=False, default='')
    favor = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        db_table = 'guilds'
        managed = False


class GuildMembers(models.Model):
    """
    This model maps to the guild_members table in the database.
    """

    def __str__(self):
        return str(self.char_id)

    char_id = models.OneToOneField(Characters, on_delete=models.RESTRICT, db_column='char_id', primary_key=True)
    guild_id = models.ForeignKey(Guilds, on_delete=models.RESTRICT, db_column='guild_id')
    rank = models.PositiveSmallIntegerField(null=False, default=0)
    tribute_enable = models.PositiveSmallIntegerField(null=False, default=0)
    total_tribute = models.PositiveIntegerField(null=False, default=0)
    last_tribute = models.PositiveIntegerField(null=False, default=0)
    banker = models.PositiveSmallIntegerField(null=False, default=0)
    public_note = models.TextField(null=False)
    alt = models.PositiveSmallIntegerField(null=False, default=0)
    online = models.PositiveSmallIntegerField(null=False, default=0)

    class Meta:
        db_table = 'guild_members'
        managed = False


class GuildRanks(models.Model):
    """
    Maps to guild_ranks — per-guild custom rank title overrides.
    Composite PK (guild_id, rank); guild_id declared primary_key for Django compatibility.
    """

    guild_id = models.IntegerField(primary_key=True, default=0, db_column='guild_id')
    rank = models.PositiveSmallIntegerField(null=False, default=0)
    title = models.CharField(max_length=128, null=False, default='')

    class Meta:
        db_table = 'guild_ranks'
        managed = False


class GuildRelations(models.Model):
    """
    Maps to guild_relations — declared relationships between guilds.
    Composite PK (guild1, guild2); guild1 declared primary_key for Django compatibility.
    relation: 0=Neutral, 1=Ally, 2=Enemy
    """

    guild1 = models.IntegerField(primary_key=True, default=0)
    guild2 = models.IntegerField(null=False, default=0)
    relation = models.SmallIntegerField(null=False, default=0)

    class Meta:
        db_table = 'guild_relations'
        managed = False
