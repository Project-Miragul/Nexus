import json
from pathlib import Path

from django.core.management.base import BaseCommand

from spells.models import SpellScroll, SpellVendor


class Command(BaseCommand):
    help = "Import spell purchase data from spell_buy.json into SpellScroll/SpellVendor tables."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing SpellScroll and SpellVendor rows before importing.',
        )

    def handle(self, *args, **options):
        json_path = Path('static/spell_data/spell_buy.json')
        if not json_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {json_path}"))
            return

        with open(json_path) as f:
            data = json.load(f)

        if options['clear']:
            SpellVendor.objects.all().delete()
            SpellScroll.objects.all().delete()
            self.stdout.write("Cleared existing data.")

        scrolls_created = 0
        scrolls_updated = 0
        vendors_created = 0
        vendors_skipped = 0

        # Each spell id appears in multiple class lists but has identical
        # scroll/vendor data across classes, so we deduplicate by spell_id.
        seen_spell_ids = set()

        for class_id, spells in data.items():
            for spell in spells:
                spell_id = spell['id']
                if spell_id in seen_spell_ids:
                    continue
                seen_spell_ids.add(spell_id)

                scroll, created = SpellScroll.objects.update_or_create(
                    spell_id=spell_id,
                    defaults={
                        'spell_name': spell['name'],
                        'scroll_item_id': spell['item_id'],
                        'scroll_item_name': spell['item_name'],
                        'scroll_price': spell['item_price'],
                        'scroll_rate': spell['item_rate'],
                        'icon': spell['new_icon'],
                    },
                )
                if created:
                    scrolls_created += 1
                else:
                    scrolls_updated += 1

                if spell['purchase_location_info'] == 'None':
                    continue

                for location in spell['purchase_location_info'].split(';'):
                    parts = [p.strip() for p in location.split(',')]
                    if len(parts) < 6:
                        self.stderr.write(f"Skipping malformed location for spell {spell_id}: {location!r}")
                        continue
                    merchant_id = int(parts[0])
                    merchant_name = parts[1]
                    zone_short = parts[2]
                    zone_long = parts[3]
                    zone_id = int(parts[4])
                    zone_expansion = int(parts[5])

                    _, vc = SpellVendor.objects.get_or_create(
                        scroll=scroll,
                        merchant_id=merchant_id,
                        defaults={
                            'merchant_name': merchant_name,
                            'zone_short_name': zone_short,
                            'zone_long_name': zone_long,
                            'zone_id': zone_id,
                            'zone_expansion': zone_expansion,
                        },
                    )
                    if vc:
                        vendors_created += 1
                    else:
                        vendors_skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Scrolls: {scrolls_created} created, {scrolls_updated} updated. "
            f"Vendors: {vendors_created} created, {vendors_skipped} already existed."
        ))
