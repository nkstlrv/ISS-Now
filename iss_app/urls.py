from django.urls import path
from .views import home_view, \
    map_view, \
    SetLocationView, \
    ChangeLocationView, \
    earth_cam_view, \
    data_view, \
    station_cam_view, \
    nasa_tv_view

from django.contrib.auth.decorators import login_required

urlpatterns = [

    path("", home_view, name='home'),
    path("map/", map_view, name='map'),
    path("set-location/", login_required(SetLocationView.as_view()), name='set-location'),
    path("change-location/<int:pk>/", login_required(ChangeLocationView.as_view()), name='change-location'),
    path("earth-cam/", login_required(earth_cam_view), name='earth-view'),
    path("station-cam/", login_required(station_cam_view), name='station-view'),
    path("nasa-tv/", login_required(nasa_tv_view), name='nasa-tv'),
    path("data-view/", data_view, name='data-view'),
]
