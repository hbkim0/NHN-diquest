# Generated by Django 3.1.13 on 2022-10-31 07:10

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('ml_task', models.IntegerField()),
                ('algorithms', djongo.models.fields.JSONField()),
                ('history', djongo.models.fields.JSONField()),
                ('ext', djongo.models.fields.JSONField()),
                ('reg_date', models.DateTimeField()),
                ('reg_id', models.TextField()),
                ('mod_date', models.DateTimeField()),
                ('mod_id', models.TextField()),
            ],
            options={
                'db_table': 'models',
                'ordering': ['-_id'],
            },
        ),
    ]