from django.urls import path
from .views import home_view, map_view, map_google

urlpatterns = [

    path("", home_view, name='home'),
    path("map/", map_view, name='map'),
    path("map-google/", map_google, name='map-google'),
]