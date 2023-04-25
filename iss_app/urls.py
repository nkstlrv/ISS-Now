from django.urls import path
from .views import home_view, map_view

urlpatterns = [

    path("", home_view, name='home'),
    path("map/", map_view, name='map'),
]