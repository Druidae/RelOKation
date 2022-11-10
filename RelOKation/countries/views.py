from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from countries.models import CountriesCard
from countries.serializers import CountriesSerializers


class CountriesViewSet(ModelViewSet):
    queryset = CountriesCard.objects.all()
    serializer_class = CountriesSerializers

def sign_in(request):
    return render(request, 'sign_in.html')

def sign_up(request):
    return render(request, 'sign_up.html')

