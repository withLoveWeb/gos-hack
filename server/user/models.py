from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(
        verbose_name=_("Номер телефона"),
        blank=True,
        null=True,
    )

    first_name = models.CharField(
        max_length=128,
        verbose_name=_("Имя"),
    )

    second_name = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        verbose_name=_("Фамилия"),
    )

    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        verbose_name=_("Отчество"),
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Дата рождения"),
    )

    def __str__(self):
        return (f"{self.first_name} {self.email}") 


class UserTravelHistory(models.Model):
    user = models.ForeignKey(
        "user.UserProfile", 
        on_delete=models.SET_NULL, 
        related_name='search_history',
        verbose_name=_("Пользователь"),
        null=True,
        blank=True,
    )
    ship = models.ForeignKey(
        "ship.Ship", 
        on_delete=models.SET_NULL, 
        related_name='search_history',
        verbose_name=_("Корабль"),
        null=True,
        blank=True,
    )
    start_location = models.CharField(
        max_length=255, 
        verbose_name=_("Стартовая точка"),
    )
    end_location = models.CharField(
        max_length=255, 
        verbose_name=_("Конечная точка"),
    )
    travel_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Дата и время поездки"),
    )
    in_travel_time = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name=_("Время поездки в минутах"),
    )


class AvatarPhoto(models.Model):
    avatar_id = models.AutoField(primary_key=True)
    avatar_image = models.ImageField(
        upload_to='avatar_image/',
        verbose_name=_("Аватарка"),
    )

