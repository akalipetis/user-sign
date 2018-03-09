import io
import os
import tempfile

import gnupg

from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE,
    )
    verified = models.BooleanField(default=False)

    def is_signature_valid(self, data, sig):
        """
        Returns if the given signature belongs to this user.
        """
        if self.verified == False:
            return False

        key = self.publickey_set.filter(
            fingerprint=PublicKey.verify(data, sig).fingerprint,
        ).first()
        return key

    def __str__(self):
        return str(self.user)


class PublicKey(models.Model):
    """
    Public keys contain the public key finger prints of the different public
    keys of users.
    """
    profile = models.ForeignKey(
        'signatures.UserProfile', editable=False, on_delete=models.CASCADE,
    )
    fingerprint = models.CharField(max_length=128, unique=True, editable=False)
    key = models.TextField()

    @classmethod
    def verify(cls, data, sig):
        """
        Returns the verification for the given data and signature
        """
        data_file = tempfile.mktemp()
        with open(data_file, 'w+b') as fout:
            fout.write(data.read())
        verification = settings.GPG.verify_file(sig, data_file)
        os.unlink(data_file)
        return verification

    @classmethod
    def key_for_signature(self, data, sig):
        """
        Returns the key, if any, for the given signature.
        """
        verification = self.verify(data, sig)
        return PublicKey.objects.filter(
            fingerprint=verification.fingerprint,
            profile__verified=True,
        ).first()

    def is_signature_valid(self, data, sig):
        """
        Returns if the given signature belongs to the user owning this key.
        """
        fingerprint = self.verify(data, sig).fingerprint
        if fingerprint == self.fingerprint:
            return self
        return None

    def __str__(self):
        return self.fingerprint
