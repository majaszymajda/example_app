from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def update_password(self, new_password):
        self.set_password(new_password)
        AuthToken.objects.filter(user_id=self.id).delete()

    def create_token(self):
        _, token = AuthToken.objects.create(user=self, expiry=timedelta(minutes=30))
        return token

