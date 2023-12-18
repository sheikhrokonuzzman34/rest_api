from rest_framework import serializers
from .models import MyUser

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

MyUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'name', 'email', 'tc', 'password', 'password2')

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2', '')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)  # Remove password2 from validated_data

        validate_password(password)

        user = MyUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)    
    
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'name', 'email', 'tc')    
