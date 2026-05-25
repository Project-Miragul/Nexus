import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps

SEED_MODELS = [
    "patch.PatchTag",
    "patch.PatchMessage",
    "spells.SpellExpansion",
    "spells.SpellScroll",
    "spells.SpellVendor",
    "spells.SpellPatchHistory",
    "items.ItemExpansionIdRange",
    "items.ItemExpansion",
    "items.BISEntry",
    "items.BISRevision",
    "items.ItemPatchHistory",
    "npcs.NpcPage",
    "npcs.NPCPatchHistory",
    "zones.ZonePage",
    "zones.ZonePatchHistory",
    "quests.Faction",
    "quests.QuestCategory",
    "quests.QuestTag",
    "quests.Quests",
    "quests.ItemReward",
    "quests.ExperienceReward",
    "quests.CurrencyReward",
    "quests.FactionReward",
    "quests.SkillReward",
    "quests.SpellReward",
    "quests.TitleReward",
    "quests.AAReward",
    "quests.AccessReward",
    "quests.QuestFaction",
    "quests.QuestItem",
    "quests.QuestPatchHistory",
    "quests.QuestsRelatedNPC",
    "quests.QuestsRelatedZone",
    "petitions.PetitionCategory",
]


class Command(BaseCommand):
    help = "Dump static/shared reference data as a Django fixture for seeding new installations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="fixtures/seed_data.json",
            help="Output path for the fixture file (default: fixtures/seed_data.json)",
        )

    def handle(self, *args, **options):
        output_path = options["output"]
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        self.stdout.write("Row counts:")
        total = 0
        for label in SEED_MODELS:
            app_label, model_name = label.split(".")
            try:
                model = apps.get_model(app_label, model_name)
                count = model.objects.count()
                self.stdout.write(f"  {label:<45} {count:>6}")
                total += count
            except LookupError:
                self.stdout.write(self.style.WARNING(f"  {label} — model not found, skipping"))

        self.stdout.write(f"  {'TOTAL':<45} {total:>6}")
        self.stdout.write("")

        self.stdout.write(f"Writing fixture to {output_path} ...")
        call_command(
            "dumpdata",
            *SEED_MODELS,
            output=output_path,
            indent=2,
            verbosity=0,
        )
        self.stdout.write(self.style.SUCCESS(f"Done. Load with: python manage.py loaddata {output_path}"))
