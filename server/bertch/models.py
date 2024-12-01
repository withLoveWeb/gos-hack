from django.db import models


class Bertch(models.Model):

    bertch_id = models.BigAutoField(primary_key=True)
    location = models.CharField(max_length=256)
    ship_capasity = models.PositiveSmallIntegerField(default=0)
    max_ship_capasity = models.PositiveSmallIntegerField(null=False, default=1)
