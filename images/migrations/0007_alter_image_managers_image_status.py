# Generated by Django 4.1.1 on 2022-09-14 20:25

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0006_alter_image_managers"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="image",
            managers=[
                ("object", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="image",
            name="status",
            field=models.CharField(
                choices=[("draft", "DRAFT"), ("published", "PUBLISHED")],
                default="published",
                max_length=10,
            ),
        ),
    ]