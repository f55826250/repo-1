from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import os

# Create your models here.

def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1].lower()  # Get file extension
    valid_extensions = ['.mp4', '.mkv']
    if ext not in valid_extensions:
        raise ValidationError('Invalid file format. Only MP4 and MKV files are allowed.')

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()  # Get file extension
    valid_extensions = [".png"]
    if ext not in valid_extensions:
        raise ValidationError('Invalid file format. Only PNG files are allowed.')

class Genre(models.Model):
    genre = models.TextField(default="")
    
    def __str__(self):
        return self.genre

class Film(models.Model):
    title = models.TextField(default="")
    upload = models.FileField(upload_to ='films', validators=[validate_video_extension])
    poster = models.FileField(upload_to ='posters', validators=[validate_image_extension], default="")
    genre = models.ManyToManyField(Genre, default="", related_name="Films")
    description = models.TextField(default="")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=3)

    def __str__(self):
        return self.title

class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(default="")
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ]
    )

    def __str__(self):
        return f"{self.user} reviewed the film: {self.film}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)