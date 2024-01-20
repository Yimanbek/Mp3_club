from django.db import models
from django.contrib.auth import get_user_model
from music.models import Music
# Create your models here.
class Like(models.Model):
    owner = models.ForeignKey(get_user_model(),related_name = 'likes',on_delete=models.CASCADE)
    music = models.ForeignKey(Music,related_name = 'likes',on_delete=models.CASCADE)