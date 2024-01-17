from django.db import models
from account.models import CustomUser
from django.contrib.auth import get_user_model
# Create your models here.

class Albums(models.Model):
    title = models.CharField(max_length = 255)
    owner = models.ForeignKey(get_user_model(),related_name = 'albums',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='album_images/', null=True, blank=True)
    

    def __str__(self):
        return self.title