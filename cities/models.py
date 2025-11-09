from django.db import models
from core.models import AbstractBaseIdHexUUID, AbstractBaseDateTime


class City(AbstractBaseIdHexUUID, AbstractBaseDateTime):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'

class CityTemperature(AbstractBaseIdHexUUID, AbstractBaseDateTime):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        db_table = 'city_temperature'
