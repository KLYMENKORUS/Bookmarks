# Generated by Django 4.1.1 on 2022-09-27 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("actions", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="action",
            old_name="verd",
            new_name="verb",
        ),
    ]
