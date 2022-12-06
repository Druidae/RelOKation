from django.db import models
from django.contrib.auth.models import User


class CountriesCard(models.Model):
    country_name = models.CharField(max_length=255)
    currancy = models.CharField(max_length=25)
    iso_4217_code = models.CharField(max_length=3)
    driving_side = models.CharField(max_length=255)
    calling_code = models.CharField(max_length=255)
    internet_tld = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_country')
    reader = models.ManyToManyField(User, through='UserCountriesRelation', related_name='reader_countries')

    def __str__(self):
        return f'{self.country_name}'


class UserCountriesRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    countries = models.ForeignKey(CountriesCard, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    is_bookmarks = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username}: {self.countries}'
    