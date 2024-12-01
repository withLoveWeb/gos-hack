from django.db import models

class Ship(models.Model):

  ship_id = models.BigAutoField(primary_key=True)

  name = models.CharField(max_length=64)
  capcity = models.IntegerField(null=False)
  max_capcity = models.IntegerField(null=False)
