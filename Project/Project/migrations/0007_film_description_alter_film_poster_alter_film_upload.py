# Generated by Django 5.1.3 on 2024-11-16 20:11

import Project.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Project", "0006_remove_film_genre_film_genre"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="film",
            name="poster",
            field=models.FileField(
                default="",
                upload_to="posters",
                validators=[Project.models.validate_image_extension],
            ),
        ),
        migrations.AlterField(
            model_name="film",
            name="upload",
            field=models.FileField(
                upload_to="films", validators=[Project.models.validate_video_extension]
            ),
        ),
    ]
