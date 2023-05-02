# Generated by Django 4.2 on 2023-05-02 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("iss_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="location",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Notify",
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
                ("do_notify", models.BooleanField(default=True)),
                ("last_notified", models.IntegerField(default=None, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notify",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
