from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        music = attrs['music']
        if user.likes.filter(music=music).exists():
            raise serializers.ValidationError(
                'You have already liked this music!'
            )
        return attrs

