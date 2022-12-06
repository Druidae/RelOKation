
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from countries.models import CountriesCard
from countries.models import UserCountriesRelation


@admin.register(CountriesCard)
class CountriesAdmin(ModelAdmin):
    pass

@ admin.register(UserCountriesRelation)
class UserCountriesRelationAdmin(ModelAdmin):
    pass