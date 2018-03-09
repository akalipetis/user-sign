from rest_framework import authentication
from django.contrib import auth

from common import models


class TokenAuthentication(authentication.TokenAuthentication):
    """
    Authentication, using the AuthToken model as Token model.
    """
    model = models.AuthToken
