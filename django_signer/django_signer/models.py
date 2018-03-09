import requests

from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def random_token_32():
    """
    Generates a random token, consisting of 32 characters.
    """
    return get_random_string(32)


class AuthToken(models.Model):
    """
    Model used for authenticating clients against the API, using token
    authentication.
    """
    key = models.CharField(
        max_length=32, default=random_token_32, editable=False,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    def __str__(self):
        return f'{self.user.username}: {self.created_at}'
