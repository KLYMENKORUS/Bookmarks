# Generated by Django 4.1.1 on 2022-09-09 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="image",
            new_name="profile_photo",
        ),
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.CharField(max_length=500),
        ),
    ]
