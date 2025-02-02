# Generated by Django 5.1.3 on 2024-11-16 13:26

import Project.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Project", "0003_review_description_alter_film_upload"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="poster",
            field=models.FileField(
                default="",
                upload_to="uploads/poster",
                validators=[Project.models.validate_image_extension],
            ),
        ),
    ]
