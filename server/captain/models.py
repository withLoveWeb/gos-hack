from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Captain(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=64, blank=True, null=True)
    surname = models.CharField(max_length=64, blank=True, null=True)
    lastname = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=128, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    hash_password = models.CharField(max_length=256)

    rate = models.IntegerField(default=50)
    avatar = models.ForeignKey(
        "user.AvatarPhoto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        self.hash_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.hash_password)

    def __str__(self):
        return f"{self.name} {self.surname or ''}"
