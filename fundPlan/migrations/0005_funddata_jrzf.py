# Generated by Django 3.0.7 on 2021-07-09 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundPlan', '0004_auto_20210709_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='funddata',
            name='jrzf',
            field=models.FloatField(default=0, max_length=20),
        ),
    ]
