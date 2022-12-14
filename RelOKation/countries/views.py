from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from countries.models import CountriesCard, UserCountriesRelation
from countries.serializers import CountriesSerializers, UserCountriesRelationSerializers
from countries.permissions import IsOwnerOrStaffOrReadOnly


# This class set serializers and filters setting
class CountriesViewSet(ModelViewSet):
    queryset = CountriesCard.objects.all()
    serializer_class = CountriesSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['currancy', 'calling_code', 'iso_4217_code','description']
    search_fields = ['country_name', 'id']
    ordering_fields = ['country_name']

    # This function add owner to the created object
    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserCountriesRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserCountriesRelation.objects.all()
    serializer_class = UserCountriesRelationSerializers
    lookup_field = 'countries'

    def get_object(self):
        obj, created = UserCountriesRelation.objects.get_or_create(user = self.request.user, countries_id = self.kwargs['countries'])

        print('created', created)
        return obj



def main_page(request):
    return render(request, 'main_goest_user.html')

def sign_in(request):
    return render(request, 'sign_in.html')

def sign_up(request):
    return render(request, 'sign_up.html')

