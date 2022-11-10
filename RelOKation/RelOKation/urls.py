from django.contrib import admin
from rest_framework.routers import SimpleRouter
from django.urls import re_path as url
from django.urls import path


from countries.views import CountriesViewSet

router = SimpleRouter()

router.register(r'countries', CountriesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls