from django.db import models

from common.models.items import Items


class TradeskillRecipe(models.Model):
    """
    This model maps to the tradeskill_recipe table in the database.
    """
    def __str__(self):
        return str(self.name)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, default='')
    tradeskill = models.SmallIntegerField(null=False, default=0)
    skill_needed = models.SmallIntegerField(null=False, default=0, db_column='skillneeded')
    trivial = models.SmallIntegerField(null=False, default=0)
    no_fail = models.SmallIntegerField(null=False, default=0, db_column='nofail')
    replace_container = models.SmallIntegerField(null=False, default=0)
    notes = models.TextField(null=True, blank=True)
    must_learn = models.SmallIntegerField(null=False, default=0)
    learned_by_item_id = models.IntegerField(null=False, default=0)
    quest = models.SmallIntegerField(null=False, default=0)
    enabled = models.SmallIntegerField(null=False, default=1)
    min_expansion = models.SmallIntegerField(null=False, default=-1)
    max_expansion = models.SmallIntegerField(null=False, default=-1)
    content_flags = models.CharField(max_length=100, null=True, default=None)
    content_flags_disabled = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = 'tradeskill_recipe'
        managed = False


class TradeskillRecipeEntries(models.Model):
    """
    This model maps to the tradeskill_recipe_entries table in the database.
    """
    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True)
    recipe_id = models.IntegerField(null=False, default=0)
    item_id = models.ForeignKey(Items, on_delete=models.DO_NOTHING, db_column='item_id')
    success_count = models.SmallIntegerField(null=False, default=0, db_column='successcount')
    fail_count = models.SmallIntegerField(null=False, default=0, db_column='failcount')
    component_count = models.SmallIntegerField(null=False, default=1, db_column='componentcount')
    salvage_count = models.SmallIntegerField(null=False, default=0, db_column='salvagecount')
    is_container = models.SmallIntegerField(null=False, default=0, db_column='iscontainer')

    class Meta:
        db_table = 'tradeskill_recipe_entries'
        managed = False

