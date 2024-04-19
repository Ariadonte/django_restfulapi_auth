import uuid

from rest_framework import serializers
from .models import User
import datetime

from dynamic_preferences.registries import global_preferences_registry

global_preferences = global_preferences_registry.manager()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['name']:
            data['name'] = ""
        return data


class UserRefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['refresh_token']

    def update(self, instance, validated_data):
        instance.refresh_token = uuid.uuid4()
        instance.exp_date = (datetime.datetime.utcnow() +
                             datetime.timedelta(days=global_preferences['general__refresh_token_expire_time_in_days']))
        instance.save()
        return instance


class UserDeleteTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['refresh_token']

    def update(self, instance, validated_data):
        instance.refresh_token = None
        instance.exp_date = None
        instance.save()
        return instance
