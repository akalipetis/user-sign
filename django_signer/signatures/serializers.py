from rest_framework import serializers

from signatures import models


class UserProfileSerializer(serializers.ModelSerializer):
    keys = serializers.SlugRelatedField(
        many=True, slug_field='fingerprint', read_only=True,
        source='publickey_set',
    )
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = models.PublicKey
        fields = ('username', 'keys', 'first_name', 'last_name')


class PublicKeySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='profile', read_only=True)

    class Meta:
        model = models.PublicKey
        fields = ('fingerprint', 'user', 'key')


class VerifySerializer(serializers.Serializer):
    signature = serializers.FileField(required=True)
    data = serializers.FileField(required=True)
