# Generated by Django 4.1.3 on 2022-12-07 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0009_alter_countriescard_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercountriesrelation',
            old_name='is_bookmarks',
            new_name='in_bookmarks',
        ),
    ]
