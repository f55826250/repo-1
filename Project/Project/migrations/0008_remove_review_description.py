# Generated by Django 5.1.3 on 2024-11-17 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Project", "0007_film_description_alter_film_poster_alter_film_upload"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="description",
        ),
    ]
