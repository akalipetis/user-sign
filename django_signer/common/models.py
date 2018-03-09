"""
Common models, used throughout the project.
"""
import uuid

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string


def random_token_32():
    """
    Generates a random token, consisting of 32 characters.
    """
    return get_random_string(32)


class BaseModel(models.Model):
    """
    Base model, having UUID as the PK, created_at and updated_at fields.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class AuthToken(BaseModel):
    """
    Model used for authenticating clients against the API, using token
    authentication.
    """
    key = models.CharField(
        max_length=32, default=random_token_32, editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE,
    )
    user_agent = models.CharField(blank=True, max_length=512)

    def __str__(self):
        return f'{self.user.username} / {self.user_agent}'
