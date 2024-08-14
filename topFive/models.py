from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    team_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'topFive'
        # Ensure that CustomUser is used instead of the default User model
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    # Override the related_name attributes for the reverse relationships
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Ensure unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Ensure unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )
