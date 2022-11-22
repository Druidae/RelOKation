from countries.models import CountriesCard
from django.contrib import admin
from django.contrib.admin import ModelAdmin


@admin.register(CountriesCard)
class CountriesAdmin(ModelAdmin):
    pass