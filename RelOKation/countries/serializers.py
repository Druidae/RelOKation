from rest_framework.serializers import ModelSerializer

from countries.models import CountriesCard, UserCountriesRelation

class CountriesSerializers(ModelSerializer):
    class Meta:
        model = CountriesCard
        # If you need concrete filters(like id or name or something else), use 
        #fields = ('id', 'name')
        fields = '__all__'


class UserCountriesRelationSerializers(ModelSerializer):
    class Meta:
        model = UserCountriesRelation
        # If you need concrete filters(like id or name or something else), use 
        #fields = ('id', 'name')
        fields = ('countries', 'like', 'in_bookmarks')