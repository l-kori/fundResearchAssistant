# Generated by Django 2.1 on 2021-07-17 12:45

from django.db import migrations, models
import django.db.models.query


class Migration(migrations.Migration):

    dependencies = [
        ('fundPlan', '0011_auto_20210717_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fundlist',
            old_name='fundprofitrate',
            new_name='fundProfitRate',
        ),
        migrations.AddField(
            model_name='fundlist',
            name='fundProfitMoney',
            field=models.FloatField(default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='fundlist',
            name='isbuy',
            field=models.IntegerField(default=0, null=django.db.models.query.FlatValuesListIterable),
        ),
    ]
