# Generated by Django 3.0.7 on 2021-07-09 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundPlan', '0002_auto_20210707_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='funddata',
            name='pjzf',
            field=models.IntegerField(default=0, max_length=20),
        ),
    ]
