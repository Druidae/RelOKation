from rest_framework.serializers import ModelSerializer

from countries.models import CountriesCard

class CountriesSerializers(ModelSerializer):
    class Meta:
        model = CountriesCard
        # If you need concrete filters(like id or name or something else), use 
        #fields = ('id', 'name')
        fields = '__all__'


class UserCountriesRelationSerializers(ModelSerializer):
    class Meta:
        model = CountriesCard
        # If you need concrete filters(like id or name or something else), use 
        #fields = ('id', 'name')
        fields = ('countries', 'like', 'is_bookmarks')