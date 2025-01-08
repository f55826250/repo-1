# Generated by Django 5.1.3 on 2024-11-15 14:30

import Project.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Project", "0002_alter_film_upload_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="film",
            name="upload",
            field=models.FileField(
                upload_to="uploads/films",
                validators=[Project.models.validate_video_extension],
            ),
        ),
    ]