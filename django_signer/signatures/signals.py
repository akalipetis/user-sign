"""
Signals hooking logic to database changes for the signatures.
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver

from signatures import models


@receiver(signals.post_save, sender=User, dispatch_uid='create_profile')
def create_profile(sender, instance, created=False, **kwargs):
    if not created:
        return

    models.UserProfile.objects.create(user=instance)


@receiver(signals.pre_save, sender=models.PublicKey, dispatch_uid='init_key')
def init_key(sender, instance, *args, **kwargs):
    if instance.fingerprint:
        return

    result = settings.GPG.import_keys(instance.key)
    if len(result.fingerprints):
        instance.fingerprint = result.fingerprints[0]
