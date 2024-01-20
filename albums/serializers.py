from rest_framework import serializers
from .models import Albums

class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Albums
        fields = ['title', 'image', 'owner']

    def create(self, validated_data):
        user = self.context['request'].user
        album = Albums.objects.create(owner=user, **validated_data)
        return album

class AlbumDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Albums
        fields = ['id', 'title', 'image', 'owner']
