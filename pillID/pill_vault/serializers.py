
from rest_framework import serializers

from .models import Pill, PillIntake, PillReminder

# For Admin OPS
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("HERE")
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if validated_data.get('password'):
            instance.password = make_password(validated_data.get('password'))
        instance.save()
        return instance

class PillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pill
        fields = ['name', 'color', 'imprint', 'shape']

class ScrapedPillSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=255)
    imprint = serializers.CharField(max_length=255)
    color = serializers.CharField(max_length=255)
    shape = serializers.CharField(max_length=255)
    # Include other fields as necessary

    def create(self, validated_data):
        # Logic to create and return a new Pill object from validated data
        # print('validated_data = ', validated_data)
        return Pill.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Optional: Logic to update an existing Pill object with validated data
        # print('validated_data2 = ', validated_data)

        instance.name = validated_data.get('name', instance.name)
        instance.imprint = validated_data.get('imprint', instance.imprint)
        instance.color = validated_data.get('Color', instance.color)
        instance.shape = validated_data.get('Shape', instance.shape)
        # Update other fields as necessary
        instance.save()
        return instance


class PillIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PillIntake
        fields = '__all__'

class PillReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PillReminder
        fields = '__all__'

class PillInfoSerializerVerbose(serializers.ModelSerializer):
    class Meta:
        model = Pill
        # fields = ('purpose', 'application', 'side_effects', 'strength', 'image', 'name', 'imprint', 'shape', 'color')
        fields = ('purpose', 'application', 'side_effects', 'strength', 'name', 'imprint', 'shape', 'color')