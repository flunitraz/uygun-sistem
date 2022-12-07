from django.db import models

# Create your models here.
class Sistem(models.Model):
    islemci = models.CharField(max_length=100)
    ekran_karti = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    depolama = models.CharField(max_length=100)
    fiyat = models.IntegerField()
    satici = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    img = models.CharField(max_length=300)