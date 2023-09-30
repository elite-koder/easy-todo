from django.contrib.auth.models import AbstractUser
from base.models import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    def get_session_auth_hash(self):
        return "qwerty"
