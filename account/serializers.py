from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation', 'first_name', 'last_name', 'username')
    
    
    def validate(self, attrs):
        password = attrs['password']
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError(
                'Passwords must be the same'
            )
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'The password must contain letters and numbers'
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        self.code = attrs['code']
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(activation_code=self.code)
            user.is_active = True
            user.activation_code = ''
            user.save()
        except:
            raise serializers.ValidationError('неверный код')
    



class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_change_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password_confirmation', 'password_change_code')

    def validate(self, attrs):
        password = attrs['password']
        password_confirmation = attrs['password_confirmation']
        password_change_code = attrs['password_change_code']

        if password != password_confirmation:
            raise serializers.ValidationError('Пароли должны совпадать')

        if not (any(char.isdigit() for char in password) and any(char.isalpha() for char in password)):
            raise serializers.ValidationError('Пароль должен содержать буквы и цифры')

        instance = self.instance
        if instance and instance.password_change_code != password_change_code:
            raise serializers.ValidationError('Неверный код изменения пароля')

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.password_change_code = ''
        instance.save()
        return instance
