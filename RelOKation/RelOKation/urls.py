from django.contrib import admin
from rest_framework.routers import SimpleRouter
from django.urls import include, re_path as url
from django.urls import path


from countries.views import CountriesViewSet
from countries.views import main_page, sign_up

router = SimpleRouter()

router.register(r'countries', CountriesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('', main_page),
    path('register/', sign_up)
]

urlpatterns += router.urls