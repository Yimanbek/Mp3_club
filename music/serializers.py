from rest_framework import serializers
from .models import Music
from like.serializers import LikeSerializer



class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'name_music', 'audio_file', 'image_music', 'author', 'category', 'in_albums']
from rest_framework import serializers




class MusicOutputSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

    def get_audio_file_url(self, obj):
        return obj.audio_file.url  




class MusicOutputSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Music
        fields = '__all__'
