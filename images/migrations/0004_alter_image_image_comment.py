# Generated by Django 4.1.1 on 2022-09-14 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0003_remove_image_url_alter_image_image_alter_image_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="images", verbose_name="Your images:"
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        help_text="Enter your comment",
                        max_length=500,
                        verbose_name="Your comment:",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="images.image",
                    ),
                ),
            ],
            options={
                "ordering": ("created",),
            },
        ),
    ]