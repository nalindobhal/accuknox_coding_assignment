from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from config import settings


class CustomUserManager(UserManager):

    def create_superuser(self, email=None, password=None, **extra_fields):
        # overriding this to create superuser with email.
        # Since USERNAME_FIELD is pointing to "email", createsuperuser will raise error since
        # create_superuser method requires username as positional argument.
        username = email.split('@')[0]
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField("email address", blank=True, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'{self.id} - {self.username}'


class FriendRequest(models.Model):
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"

    __STATUS_CHOICES = [(i, i) for i in [STATUS_ACCEPTED, STATUS_REJECTED]]

    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_by', on_delete=models.CASCADE)
    sent_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_to', on_delete=models.CASCADE)

    status = models.CharField(max_length=16, choices=__STATUS_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Last Updated", auto_now=True)

    class Meta:
        db_table = 'friend_request'
        constraints = [
            models.UniqueConstraint(fields=['sent_by', 'sent_to', 'status'], name='unique_friend_request_constraint')
        ]

    def __str__(self):
        return f'Id: {self.id} --> Sent By: {self.sent_by_id} --> Sent To: {self.sent_to_id}'


class Friends(models.Model):
    my_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name="my_user")
    my_friend = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="my_friend"
    )
    created_at = models.DateTimeField(verbose_name="Created", auto_now_add=True)

    class Meta:
        db_table = 'friends'
        constraints = [
            models.UniqueConstraint(fields=['my_user', 'my_friend'], name='unique_friend__constraint')
        ]

    def __str__(self):
        return f'Id: {self.id} --> My User: {self.my_user_id} --> Friend: {self.my_friend_id}'
