from django.contrib import admin

from spells.models import SpellExpansion, SpellPatchHistory, SpellScroll, SpellVendor


@admin.register(SpellExpansion)
class SpellExpansionAdmin(admin.ModelAdmin):
    list_display = ('id', 'spell_name', 'expansion')
    list_filter = ('expansion',)
    search_fields = ('id', 'spell_name')


class SpellVendorInline(admin.TabularInline):
    model = SpellVendor
    extra = 0
    fields = ('merchant_id', 'merchant_name', 'zone_short_name', 'zone_long_name', 'zone_id', 'zone_expansion')


@admin.register(SpellScroll)
class SpellScrollAdmin(admin.ModelAdmin):
    list_display = ('spell_name', 'spell_id', 'scroll_item_name', 'scroll_price', 'scroll_rate', 'icon')
    search_fields = ('spell_name', 'spell_id', 'scroll_item_name')
    inlines = [SpellVendorInline]


@admin.register(SpellPatchHistory)
class SpellPatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['spell_name', 'spell_id', 'patch', 'role']
    list_filter = ['role']
    search_fields = ['spell_name', 'spell_id']
    autocomplete_fields = ['patch']
    ordering = ['patch__patch_date']
