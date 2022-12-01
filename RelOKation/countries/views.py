from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from countries.models import CountriesCard
from countries.serializers import CountriesSerializers


# This class set serializers and filters setting
class CountriesViewSet(ModelViewSet):
    queryset = CountriesCard.objects.all()
    serializer_class = CountriesSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['currancy', 'calling_code', 'iso_4217_code','description']
    search_fields = ['country_name', 'id']
    ordering_fields = ['country_name']

def sign_in(request):
    return render(request, 'sign_in.html')

def sign_up(request):
    return render(request, 'sign_up.html')

