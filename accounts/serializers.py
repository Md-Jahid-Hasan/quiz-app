from rest_framework import serializers
from django.contrib.auth import get_user_model as User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User()
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if validated_data.get('password', "") != validated_data.get('confirm_password', None):
            raise serializers.ValidationError({
                'password': ["Password Dont match"]
            })
        validated_data.pop('confirm_password')
        return super(UserSerializer, self).create(validated_data)
