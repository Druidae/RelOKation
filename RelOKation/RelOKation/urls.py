from django.contrib import admin
from rest_framework.routers import SimpleRouter
from django.urls import include, re_path as url
from django.urls import path


from countries.views import CountriesViewSet, UserCountriesRelationViewSet
from countries.views import main_page, sign_up, sign_in

router = SimpleRouter()

router.register(r'countries', CountriesViewSet)
router.register(r'countrie_relation', UserCountriesRelationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('', main_page),
    path('signup/', sign_up),
    path('signin/', sign_in)
    #url('accounts/profile/', include())
]

urlpatterns += router.urls