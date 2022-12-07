from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail

import json
import os

from countries.models import CountriesCard, UserCountriesRelation
from countries.serializers import CountriesSerializers


"""
For check code coverage by tests, use {coverage run --source='.' manage.py test .} for generate report and after thet
use {coverage report} for output result in your terminal. If you won't generate report as html format use {coverage html}
"""
class CountriesApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.countries_1 = CountriesCard.objects.create(
            country_name='countrie 1', 
            currancy='countrie currancy', 
            iso_4217_code='CD', 
            driving_side='right', 
            calling_code='+221', 
            internet_tld='.de', 
            description='This field will be comleted later',
            owner = self.user
        )
        self.countries_2 = CountriesCard.objects.create(
            country_name='countrie 2', 
            currancy='countrie currancy 2', 
            iso_4217_code='CD2', 
            driving_side='left', 
            calling_code='+2', 
            internet_tld='.re', 
            description='This field will be comleted later',
            owner = self.user
        )
        self.countries_3 = CountriesCard.objects.create(
            country_name='countrie 3', 
            currancy='countrie currancy 3', 
            iso_4217_code='CD3', 
            driving_side='right', 
            calling_code='+1', 
            internet_tld='.se', 
            description='This field will be comleted later',
            owner = self.user
        )
    
    def test_get(self):
        url = reverse('countriescard-list')
        response = self.client.get(url)
        serializer_data = CountriesSerializers([self.countries_1, self.countries_2, self.countries_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_one(self):
        url = reverse('countriescard-detail', args=(self.countries_1.id,))
        response = self.client.get(url)
        serializer_data = CountriesSerializers(self.countries_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


    def test_get_serch(self):
        url = reverse('countriescard-list')
        response = self.client.get(url, data={'search': '+221'})
        serializer_data = CountriesSerializers([self.countries_1, self.countries_2, self.countries_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_serch(self):
        url = reverse('countriescard-list')
        response = self.client.get(url, data={'country_name': 'countrie 1'})
        serializer_data = CountriesSerializers([self.countries_1, self.countries_2, self.countries_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_created(self):
        self.assertEqual(3, CountriesCard.objects.all().count())
        url = reverse('countriescard-list')
        data = {
            'country_name': 'countrie 4',
            'currancy': 'countrie currancy 4',
            'iso_4217_code': 'CD4',
            'driving_side': 'right',
            'calling_code': '+78',
            'internet_tld': '.def',
            'description': 'This field will be comleted later'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, CountriesCard.objects.all().count())
        self.assertEqual(self.user, CountriesCard.objects.last().owner)

    def test_update(self):
        url = reverse('countriescard-detail',args=(self.countries_1.id,))
        data = {
            'country_name': self.countries_1.country_name,
            'currancy': self.countries_1.currancy,
            'iso_4217_code': self.countries_1.iso_4217_code,
            'driving_side': 'left',
            'calling_code': self.countries_1.calling_code,
            'internet_tld': self.countries_1.internet_tld,
            'description': self.countries_1.description,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.countries_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('left', self.countries_1.driving_side)

    def test_delete(self):
        self.assertEqual(3, CountriesCard.objects.all().count())
        url = reverse('countriescard-detail',args=(self.countries_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, CountriesCard.objects.all().count())

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2',)        
        url = reverse('countriescard-detail',args=(self.countries_1.id,))
        data = {
            'country_name': self.countries_1.country_name,
            'currancy': self.countries_1.currancy,
            'iso_4217_code': self.countries_1.iso_4217_code,
            'driving_side': 'left',
            'calling_code': self.countries_1.calling_code,
            'internet_tld': self.countries_1.internet_tld,
            'description': self.countries_1.description,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.countries_1.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual('right', self.countries_1.driving_side)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}, response.data)

    def test_delete_not_owner(self):
        self.user2 = User.objects.create(username='test_username2',)        
        self.assertEqual(3, CountriesCard.objects.all().count())
        url = reverse('countriescard-detail', args=(self.countries_1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, CountriesCard.objects.all().count())
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}, response.data)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('countriescard-detail', args=(self.countries_1.id,))
        data = {
            'country_name': self.countries_1.country_name,
            'currancy': self.countries_1.currancy,
            'iso_4217_code': self.countries_1.iso_4217_code,
            'driving_side': 'left',
            'calling_code': self.countries_1.calling_code,
            'internet_tld': self.countries_1.internet_tld,
            'description': self.countries_1.description,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.countries_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('left', self.countries_1.driving_side)

    def test_delete_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2',is_staff=True)
        self.assertEqual(3, CountriesCard.objects.all().count())
        url = reverse('countriescard-detail',args=(self.countries_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, CountriesCard.objects.all().count())




class CountriesSerializerTestCase(TestCase):
    def test_ok(self):
        countries_1 = CountriesCard.objects.create(country_name='countrie 1', currancy='countrie currancy', iso_4217_code='CD', driving_side='right', calling_code='+221', internet_tld='.de', description='This field will be comleted later')
        countries_2 = CountriesCard.objects.create(country_name='countrie 2', currancy='countrie currancy 2', iso_4217_code='CD2', driving_side='left', calling_code='+2', internet_tld='.re', description='This field will be comleted later')
        countries_3 = CountriesCard.objects.create(country_name='countrie 3', currancy='countrie currancy 3', iso_4217_code='CD3', driving_side='right', calling_code='+1', internet_tld='.se', description='This field will be comleted later')
        data = CountriesSerializers([countries_1, countries_2, countries_3], many=True).data
        expected_data = [
            {
                'id': countries_1.id,
                'country_name': 'countrie 1',
                'currancy': 'countrie currancy',
                'iso_4217_code': 'CD',
                'driving_side': 'right',
                'calling_code': '+221',
                'internet_tld': '.de',
                'description': 'This field will be comleted later'
            },
            {
                'id': countries_2.id,
                'country_name': 'countrie 2',
                'currancy': 'countrie currancy 2',
                'iso_4217_code': 'CD2',
                'driving_side': 'left',
                'calling_code': '+2',
                'internet_tld': '.re',
                'description': 'This field will be comleted later'
            },
            {
                'id': countries_3.id,
                'country_name': 'countrie 3',
                'currancy': 'countrie currancy 3',
                'iso_4217_code': 'CD3',
                'driving_side': 'right',
                'calling_code': '+1',
                'internet_tld': '.se',
                'description': 'This field will be comleted later'
            }
        ]

        self.assertEqual(expected_data, data)


class CountriesRelationsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.countries_1 = CountriesCard.objects.create(
            country_name='countrie 1', 
            currancy='countrie currancy', 
            iso_4217_code='CD', 
            driving_side='right', 
            calling_code='+221', 
            internet_tld='.de', 
            description='This field will be comleted later',
            owner = self.user
        )
        self.countries_2 = CountriesCard.objects.create(
            country_name='countrie 2', 
            currancy='countrie currancy 2', 
            iso_4217_code='CD2', 
            driving_side='left', 
            calling_code='+2', 
            internet_tld='.re', 
            description='This field will be comleted later',
            owner = self.user
        )
    
    def test_like(self):
        url = reverse('usercountriesrelation-detail',args=(self.countries_1.id,))
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserCountriesRelation.objects.get(user=self.user, countries = self.countries_1)
        self.assertTrue(relation.like)

        data = {
            'in_bookmarks': True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserCountriesRelation.objects.get(user=self.user, countries = self.countries_1)
        self.assertTrue(relation.in_bookmarks)

