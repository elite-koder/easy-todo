from django.contrib.auth.models import AbstractUser

from django.db import models
from base.models import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    dp_link = models.URLField(default=None, null=True)

    def get_session_auth_hash(self):
        return "qwerty"

    @property
    def name(self):
        first_name = ""
        last_name = ""
        if self.first_name:
            first_name = self.first_name
        if self.last_name:
            last_name = self.last_name
        return f"{first_name} {last_name}".strip()

    @classmethod
    def create_user(cls, email, name, dp_link):
        email = email.lower()
        first_name, last_name = name.split(" ", 1)
        return cls.objects.get_or_create(username=email, defaults={"first_name": first_name, "last_name": last_name, "email": email, "dp_link": dp_link})
