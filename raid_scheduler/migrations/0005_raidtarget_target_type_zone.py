from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raid_scheduler', '0004_alter_raidevent_status_alter_raidevent_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='raidtarget',
            name='zone',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='raidtarget',
            name='target_type',
            field=models.CharField(
                choices=[
                    ('boss',    'Boss Kill'),
                    ('event',   'Event / Trial'),
                    ('farming', 'Farming Run'),
                ],
                default='boss',
                max_length=20,
            ),
        ),
        migrations.AlterModelOptions(
            name='raidtarget',
            options={'ordering': ['zone', 'name']},
        ),
    ]
