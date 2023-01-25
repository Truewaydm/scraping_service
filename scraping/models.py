from django.db import models


# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='City name', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'City name'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Language', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name
