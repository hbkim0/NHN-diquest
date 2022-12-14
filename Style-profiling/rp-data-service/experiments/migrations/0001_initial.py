# Generated by Django 3.1.13 on 2022-11-15 09:25

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('model_id', models.TextField()),
                ('seq_num_major', models.IntegerField()),
                ('seq_num_minor', models.IntegerField()),
                ('status', models.IntegerField()),
                ('serving', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('parameters', djongo.models.fields.JSONField()),
                ('rmse', models.FloatField()),
                ('history', djongo.models.fields.JSONField()),
                ('ext', djongo.models.fields.JSONField()),
                ('reg_date', models.DateTimeField()),
                ('reg_id', models.TextField()),
                ('mod_date', models.DateTimeField()),
                ('mod_id', models.TextField()),
            ],
            options={
                'db_table': 'experiments',
                'ordering': ['-_id'],
            },
        ),
    ]
