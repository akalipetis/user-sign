from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe

from signatures import models


class PublicKeyInlineAdmin(admin.TabularInline):
    """
    Admin model for the user profiles.
    """
    model = models.PublicKey
    readonly_fields = ('fingerprint', 'key',)
    extra = 0


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin model for the user profiles.
    """
    list_display = ('user',)
    readonly_fields = ('user', 'user_link')
    inlines = [PublicKeyInlineAdmin]

    def user_link(self, instance):
        url = reverse(
            'admin:auth_user_change', args=(instance.user.pk,),
        )
        return mark_safe(f'<a href="{url}">User details</a>')
