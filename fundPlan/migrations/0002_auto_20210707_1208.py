# Generated by Django 3.0.7 on 2021-07-07 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fundPlan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funddata',
            name='gztime',
        ),
        migrations.RemoveField(
            model_name='funddata',
            name='zxjz',
        ),
        migrations.RemoveField(
            model_name='funddata',
            name='zxzf',
        ),
    ]