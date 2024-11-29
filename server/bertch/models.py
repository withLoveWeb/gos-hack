from django.db import models


class Bertch(models.Model):

    bertch_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_lenth=256)
    ship_capasity = models.SmallAutoField(defaul=0)
    max_ship_capasity = models.SmallAutoField(null=False, default=1)
