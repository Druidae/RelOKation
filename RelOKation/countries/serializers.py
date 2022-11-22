from rest_framework.serializers import ModelSerializer

from countries.models import CountriesCard

class CountriesSerializers(ModelSerializer):
    class Meta:
        model = CountriesCard
        fields = '__all__'