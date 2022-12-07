# Generated by Django 3.1.13 on 2022-10-27 08:04

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('dataset_id', models.TextField()),
                ('bundle_id', models.TextField()),
                ('file_id', models.TextField()),
                ('versioned_dataset_id', models.TextField()),
                ('description', models.TextField()),
                ('done', models.IntegerField()),
                ('split', models.IntegerField(blank=True, null=True)),
                ('labels', djongo.models.fields.JSONField()),
                ('history', djongo.models.fields.JSONField()),
                ('ext', djongo.models.fields.JSONField()),
                ('reg_date', models.DateTimeField()),
                ('reg_id', models.TextField()),
                ('mod_date', models.DateTimeField()),
                ('mod_id', models.TextField()),
            ],
            options={
                'db_table': 'annotations',
                'ordering': ['-_id'],
            },
        ),
    ]
