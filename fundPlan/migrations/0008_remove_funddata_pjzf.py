# Generated by Django 3.0.7 on 2021-07-14 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fundPlan', '0007_auto_20210714_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funddata',
            name='pjzf',
        ),
    ]
