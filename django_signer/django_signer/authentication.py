from rest_framework import authentication
from django.contrib import auth

from django_signer import models


class TokenAuthentication(authentication.TokenAuthentication):
    """
    Authentication, using the AuthToken model as Token model.
    """
    model = models.AuthToken
