# Generated by Django 3.0.7 on 2021-07-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundPlan', '0008_remove_funddata_pjzf'),
    ]

    operations = [
        migrations.AddField(
            model_name='funddata',
            name='jdzjrzf',
            field=models.FloatField(default=0, max_length=20),
        ),
    ]
