from django.db import models
from category.models import Category
from django.contrib.auth import get_user_model
from albums.models import Albums

class Music(models.Model):
    name_music = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='music_mp3/')
    image_music = models.ImageField(upload_to='music_images/',default='/home/yimanbek/Desktop/project_mp3/music/defaul_image/sEZB30zciy5YEGCrSUPkhKNMjcXUm7YdvC0PwpwIYZ3CRmhrXUDBnGwbKnN-ya9Z4VSnrqwe.jpg',blank=True)
    author = models.ForeignKey(get_user_model(), related_name='music', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='music')
    in_albums = models.ForeignKey(Albums, related_name='music', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name_music