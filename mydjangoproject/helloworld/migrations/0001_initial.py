# Generated by Django 4.2.2 on 2023-06-21 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "city",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("description", models.CharField(max_length=400)),
            ],
        ),
    ]
