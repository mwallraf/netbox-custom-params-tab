# WARNING: This migration was hand-crafted because NetBox was not installed at
# generation time. It MUST be regenerated before deploying against a real NetBox
# database:
#
#   pip install netbox  # or install from source
#   python -m django makemigrations netbox_custom_field_profiles --settings=testing.settings
#
# Known issues in this hand-crafted version:
#   - custom_field_data uses encoder=None instead of NetBox's custom encoder
#   - managers declaration for RestrictedManager is absent

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('extras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomTabConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=None)),
                ('tab_label', models.CharField(default='Parameters', max_length=100)),
                ('enabled', models.BooleanField(default=True)),
                ('content_type', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='custom_tab_config',
                    to='contenttypes.contenttype',
                )),
            ],
            options={
                'verbose_name': 'Custom Tab Config',
                'verbose_name_plural': 'Custom Tab Configs',
                'ordering': ['content_type__app_label', 'content_type__model'],
            },
        ),
        migrations.CreateModel(
            name='CustomTabConfigGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50)),
                ('weight', models.PositiveIntegerField(default=100)),
                ('tab_config', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='config_groups',
                    to='netbox_custom_field_profiles.customtabconfig',
                )),
            ],
            options={
                'ordering': ['weight', 'group_name'],
                'unique_together': {('tab_config', 'group_name')},
            },
        ),
        migrations.CreateModel(
            name='CustomTabConfigField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField(default=100)),
                ('tab_config', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='config_fields',
                    to='netbox_custom_field_profiles.customtabconfig',
                )),
                ('field', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='extras.customfield',
                )),
            ],
            options={
                'ordering': ['weight', 'field__name'],
                'unique_together': {('tab_config', 'field')},
            },
        ),
        migrations.AddField(
            model_name='customtabconfig',
            name='fields',
            field=models.ManyToManyField(
                blank=True,
                related_name='custom_tab_configs',
                through='netbox_custom_field_profiles.CustomTabConfigField',
                to='extras.customfield',
            ),
        ),
    ]
