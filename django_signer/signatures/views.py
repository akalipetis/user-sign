from rest_framework import decorators, mixins, response, viewsets

from signatures import models, serializers


class PublicKeyViewSet(viewsets.ModelViewSet):
    queryset = models.PublicKey.objects.all()
    serializer_class = serializers.PublicKeySerializer
    lookup_field = 'fingerprint'

    def get_queryset(self):
        return self.request.user.userprofile.publickey_set.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.userprofile)

class PublicKeyVerificationViewSet(
    mixins.RetrieveModelMixin, viewsets.GenericViewSet,
):
    """
    ViewSet used to verify signatures against against specific keys.
    """
    queryset = models.PublicKey.objects.all()
    serializer_class = serializers.PublicKeySerializer
    lookup_field = 'fingerprint'

    @decorators.detail_route(
        methods=['POST'], serializer_class=serializers.VerifySerializer,
    )
    def verify(self, request, *args, **kwargs):
        """
        Verifies the given signature and data against a given key.
        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        key = self.get_object()
        verified_key = key.is_signature_valid(
            data=serializer.validated_data['data'].file,
            sig=serializer.validated_data['signature'].file,
        )
        key_data = None
        if verified_key is not None:
            key_data = serializers.PublicKeySerializer(verified_key).data
        return response.Response({
            'valid': verified_key is not None,
            'key': key_data,
        })


class ProfileVerificationViewSet(
    mixins.RetrieveModelMixin, viewsets.GenericViewSet,
):
    """
    ViewSet used to verify signatures against against specific users.
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    lookup_field = 'user__username'

    @decorators.detail_route(
        methods=['POST'], serializer_class=serializers.VerifySerializer,
    )
    def verify(self, request, *args, **kwargs):
        """
        Verifies the given signature and data against a user.
        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        verified_key = user.is_signature_valid(
            data=serializer.validated_data['data'].file,
            sig=serializer.validated_data['signature'].file,
        )
        key_data = None
        if verified_key is not None:
            key_data = serializers.PublicKeySerializer(verified_key).data
        return response.Response({
            'valid': verified_key is not None,
            'key': key_data,
        })
